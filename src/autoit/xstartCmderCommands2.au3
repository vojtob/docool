#include <MsgBoxConstants.au3>

Local $hWnd = WinWaitActive("[CLASS:VirtualConsoleClass]");
Local $projectDir = $CmdLine[1];
Local $dirs = StringSplit ($projectDir, "\")
Local $projectName = $dirs[$dirs[0]]
Sleep(500);

Send("cd " & $projectDir & "\utils{ENTER}");
Sleep(300);
Send("cls{ENTER}");
Sleep(200);
Send("{F2}ify{ENTER}");
Sleep(200);
; activate python environment
Send("..\env\Scripts\activate.bat{ENTER}")
Sleep(200);