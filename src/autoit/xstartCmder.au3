#include <MsgBoxConstants.au3>

Local $hWnd = WinWaitActive("[CLASS:VirtualConsoleClass]");
Local $projectDir = $CmdLine[1];
Local $dirs = StringSplit ($projectDir, "\")
Local $projectName = $dirs[$dirs[0]]
Sleep(500);

; setup specifikacia tab
Send("cd " & $projectDir & "\utils{ENTER}");
Sleep(300);
Send("cls{ENTER}");
Sleep(200);
Send("{F2}hugo{ENTER}");
Sleep(200);
Send("hugo server -D -s ..\temp\spec_local\ -t hugo-theme-docdock");
Sleep(200);

; setup utils tab
Send("^t");
Sleep(500);
Send("{TAB}" & $projectDir & "\utils{ENTER}");
Sleep(1000);
Send("{F2}" & $projectName & "{ENTER}");
Sleep(2000);
Send("%windir%\System32\cmd.exe ""/K"" C:\prg\anaconda3\Scripts\activate.bat C:\prg\anaconda3{ENTER}")
Sleep(2000);
Send("docool{ENTER}");
