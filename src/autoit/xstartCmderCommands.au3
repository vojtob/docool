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
Send("%windir%\System32\cmd.exe ""/K"" C:\Users\vbalint\Anaconda3\Scripts\activate.bat ify{ENTER}");
Sleep(200);