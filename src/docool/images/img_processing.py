from pathlib import Path
import os
import subprocess

import numpy as np
import cv2

import docool.images.rect_recognition as rr
import docool.images.rect_areas as ra
import docool.images.image_utils as image_utils

def imgrectangles(imgdef, args):
    # read image
    imgpath = args.projectdir / 'temp' / 'img_exported' / imgdef['fileName']
    if args.debug:
        print('whole image path:', imgpath)
    img = cv2.imread(str(imgpath), cv2.IMREAD_UNCHANGED)

    # convert to BW
    imgBW =image_utils.convertImage(img)
    # save BW image
    if args.debug:
        bwpath = args.projectdir / 'temp' / 'img_BW' / imgdef['fileName']
        bwpath.parent.mkdir(parents=True, exist_ok=True)           
        cv2.imwrite(str(bwpath), imgBW)
    
    # identify rectangles
    rectangles = rr.getRectangles(args, imgBW, imgdef)
    if args.verbose:
        imgrec = image_utils.rectangles2image(img, rectangles)
        recpath = args.projectdir / 'temp' / 'img_rec' / imgdef['fileName']
        recpath.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(recpath), imgrec)

    return img, rectangles


def icons2image(imgdef, args):
    if args.verbose:
        print('add icons to image {0}'.format(imgdef['fileName']))
    if not (args.projectdir / 'temp' / 'img_exported' / imgdef['fileName']).exists():
        args.problems.append('Add icons to image: file {0} does not exists !!!'.format(imgdef['fileName']))
        return

    img, rectangles = imgrectangles(imgdef, args)
    # add icons to image
    iconspath = args.projectdir / 'src_doc' / 'res' / 'icons'
    for icondef in imgdef['icons']:
        if args.debug:
            print('  add icon', icondef['iconName'])
        iconfilepath = iconspath / icondef['iconName']
        if not iconfilepath.exists():
            args.problems.append('Add icon2image: could not find icon {0} for image {1}'.format(icondef['iconName'], imgdef['fileName']))
            return
        # resize icon
        icon = cv2.imread(str(iconfilepath), cv2.IMREAD_UNCHANGED)
        s = max(icon.shape[0], icon.shape[1])
        dy = int((icondef['size']*icon.shape[0])/s)
        dx = int((icondef['size']*icon.shape[1])/s)
        icon = cv2.resize(icon, (dx,dy))

        if 'rec' in icondef:
            if args.debug:
                print('add icon by rect')
            recID = icondef['rec']
            if( recID > len(rectangles)):
                args.problems.append('Add icon2image: icon {0} for image {1} refers to non existing rectangle {2}'.format(icondef['iconName'], imgdef['fileName'], recID))
                return
            iconxy = image_utils.geticonxy(args, imgdef['fileName'], icondef['iconName'], 
            icon, rectangles[recID-1], icondef['x'], icondef['y'])
        else:
            iconxy = (icondef['x'], icondef['y'])
            if args.debug:
                print('add icon by position', iconxy)

        img = image_utils.overlayImageOverImage(img, icon, iconxy)


    imgiconpath = args.projectdir / 'temp' / 'img_icons' / imgdef['fileName']
    imgiconpath.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(imgiconpath), img)

def areas2image(imgdef, args):
    if args.verbose:
        print('add area {0} into image {1}'.format(imgdef['focus-name'], imgdef['fileName']))
    
    _, rectangles = imgrectangles(imgdef, args)
    imgpath = args.projectdir / 'temp' / 'img_icons' / imgdef['fileName']
    if args.debug:
        print('whole image path:', imgpath)
    img = cv2.imread(str(imgpath), cv2.IMREAD_UNCHANGED)
    # identify bounding polygons for areas
    polygons = []
    if 'distance' in imgdef:
        if args.debug:
            print('set distance')
        ra.set_area_gap(int(imgdef['distance']))
    for area in imgdef['areas']:
        area_rectangles = [rectangles[r-1] for r in area]            
        polygons.append(ra.find_traverse_points(area_rectangles))

    linecolor = (imgdef['linecolor'][2], imgdef['linecolor'][1], imgdef['linecolor'][0]) if 'linecolor' in imgdef else (0,0,255)
    linewidth = imgdef['linewidth'] if ('linewidth' in imgdef) else 2
    opacity = imgdef['opacity'] if 'opacity' in imgdef else 80
    if args.debug:
        print('linecolor: {0}, linewidth: {1}, opacity: {2}'.format(linecolor, linewidth, opacity))

    # add transparency to image
    mask = np.full((img.shape[0], img.shape[1]), opacity, np.uint8)
    for polygon in polygons:
        points = np.array([[p[0],p[1]] for p in polygon], np.int32)
        points = points.reshape((-1,1,2))
        # draw red polygon
        img = cv2.polylines(img, [points], True, linecolor, linewidth)
        # use mask to set transparency
        mask = cv2.fillPoly(mask, [points], 255)
    # print('orig shape', img.shape)
    if img.shape[2] < 4:
        # no transparency in image
        x = np.zeros((img.shape[0], img.shape[1], 1), img.dtype)
        # print('x shape', x.shape)
        img = np.concatenate((img, x),2)
        # img = np.hstack((img, x))
        # print('add transparency shape', img.shape)
        # print('mask shape', mask.shape)      
    img[:, :, 3] = mask
    # print('final shape', img.shape)

    imgpath = args.projectdir / 'temp' / 'img_areas' / imgdef['fileName'].replace('.png', '_{0}.png'.format(imgdef['focus-name']))
    imgpath.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(imgpath), img)
