[Setup]
AppName=Focus Mini
AppVersion=1.0
AppPublisher=hekawsh
AppPublisherURL=https://github.com/hekawsh/focusmini
AppSupportURL=https://github.com/hekawsh/focusmini
AppUpdatesURL=https://github.com/hekawsh/focusmini/releases
DefaultDirName={userappdata}\FocusMini
DefaultGroupName=Focus Mini
UninstallDisplayIcon={app}\FocusMini.exe
SetupIconFile=icon.ico
OutputDir=.
OutputBaseFilename=FocusMini_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "dist\FocusMini.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Focus Mini"; Filename: "{app}\FocusMini.exe"
Name: "{userdesktop}\Focus Mini"; Filename: "{app}\FocusMini.exe"

[Run]
Filename: "{app}\FocusMini.exe"; Description: "Launch Focus Mini"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\FocusMini.exe"