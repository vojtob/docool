Local $iPID = ShellExecute ("C:\Users\vbalint\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\Anaconda Prompt (Anaconda3).lnk", "", "", "")

Local $hWnd = WinWaitActive("Anaconda Prompt (Anaconda3)");
Local $projectDir = $CmdLine[1];
Local $dirs = StringSplit ($projectDir, "\")
Local $projectName = $dirs[$dirs[0]]
Sleep(500);

; setup specifikacia tab
Send("cd " & $projectDir & "\utils{ENTER}");
Send("conda activate ify{ENTER}");
