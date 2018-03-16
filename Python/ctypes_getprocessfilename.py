import ctypes
import sys

MAX_PATH = 256

def GetProcessFileName(pid):
	#****************#
	kernel32 = ctypes.windll.kernel32
	psapi = ctypes.windll.Psapi
	h = kernel32.OpenProcess(2035711,True,pid) # 2035711 <- PROCESS_ALL_ACCESS
	fileName = (ctypes.c_char*MAX_PATH)()
	'''
	d = kernel32.GetModuleFileNameA(h,fileName,MAX_PATH)
	print(fileName.value)
	'''
	d = psapi.GetProcessImageFileNameA(h,fileName,256)
	kernel32.CloseHandle(h)

	return str(fileName.value)

if __name__ == "__main__":
	#****************#
	sys.stdout.write("Enter PID: ")
	pid = input()
	fName = GetProcessFileName(int(pid))
	print(fName)

#***Get command line parameter of foreign process using PEB***
'''
#include <windows.h>
#include <stdio.h>
#include "Winternl.h"

typedef NTSTATUS (NTAPI *_NtQueryInformationProcess)(
    HANDLE ProcessHandle,
    DWORD ProcessInformationClass,
    PVOID ProcessInformation,
    DWORD ProcessInformationLength,
    PDWORD ReturnLength
    );

PVOID GetPebAddress(HANDLE ProcessHandle)
{
    _NtQueryInformationProcess NtQueryInformationProcess =
        (_NtQueryInformationProcess)GetProcAddress(
        GetModuleHandleA("ntdll.dll"), "NtQueryInformationProcess");
    PROCESS_BASIC_INFORMATION pbi;

    NtQueryInformationProcess(ProcessHandle, 0, &pbi, sizeof(pbi), NULL);

    return pbi.PebBaseAddress;
}

int wmain(int argc, WCHAR *argv[])
{
    int pid;
    HANDLE processHandle;
    PVOID pebAddress;
    PVOID rtlUserProcParamsAddress;
    UNICODE_STRING commandLine;
    WCHAR *commandLineContents;

    if (argc < 2)
    {
        printf("Usage: getprocesscommandline [pid]\n");
        return 1;
    }

    pid = _wtoi(argv[1]);

    if ((processHandle = OpenProcess(
        PROCESS_QUERY_INFORMATION | /* required for NtQueryInformationProcess */
        PROCESS_VM_READ, /* required for ReadProcessMemory */
        FALSE, pid)) == 0)
    {
        printf("Could not open process!\n");
        return GetLastError();
    }

    pebAddress = GetPebAddress(processHandle);

    /* get the address of ProcessParameters */
    if (!ReadProcessMemory(processHandle,
            &(((_PEB*) pebAddress)->ProcessParameters),
            &rtlUserProcParamsAddress,
            sizeof(PVOID), NULL))
    {
        printf("Could not read the address of ProcessParameters!\n");
        return GetLastError();
    }

    /* read the CommandLine UNICODE_STRING structure */
    if (!ReadProcessMemory(processHandle,
        &(((_RTL_USER_PROCESS_PARAMETERS*) rtlUserProcParamsAddress)->CommandLine),
        &commandLine, sizeof(commandLine), NULL))
    {
        printf("Could not read CommandLine!\n");
        return GetLastError();
    }

    /* allocate memory to hold the command line */
    commandLineContents = (WCHAR *)malloc(commandLine.Length);

    /* read the command line */
    if (!ReadProcessMemory(processHandle, commandLine.Buffer,
        commandLineContents, commandLine.Length, NULL))
    {
        printf("Could not read the command line string!\n");
        return GetLastError();
    }

    /* print it */
    /* the length specifier is in characters, but commandLine.Length is in bytes */
    /* a WCHAR is 2 bytes */
    printf("%.*S\n", commandLine.Length / 2, commandLineContents);
    CloseHandle(processHandle);
    free(commandLineContents);

    return 0;
}
'''
