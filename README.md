# docool
 document generation tools

Čo treba urobiť keď updatnem schému?

1. **Zmeniť pásik v téme na dxc farbu**.  hugo-theme-docdock/static/theme-flex/ribbon.png treba nahradiť mojím pásikom
1. **Zmenit font aby nebol problem so slovenskymi znakmi** hugo-theme-docdock/static/theme-flex/style.css
1. **Zmenit default názov projektu** docool\res\themes\hugo-theme-learn-master\layouts\partials\logo.html zadat názov SET NAME
  
```
  article section.page h1:first-of-type {
    margin: 3rem 0rem;
    font-family: "Helvetica", "Tahoma", "Geneva", "Arial", "Novacento Sans Wide", sans-serif;
```