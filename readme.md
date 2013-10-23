Extract Sublime Package -- extract a .sublime-package file for quick editing
============================================================================
This plugin allows you to easily extract a `.sublime-package` file for quick
editing. The package contents will be stored in subdirectory of your `Packages`
folder named after the package file. For example,
`Installed Packages/Extract Sublime Package.sublime-package` will be extracted
to `Packages/Extract Sublime Package/`. Sublime Text will prefer to load the
loose files from the `Packages` directory and will therefore pick up on any
changes you make to them. If you extract a package file that was installed by
[Package Control][pkgctrl] and then choose to uninstall the package, it will
remove the extracted files as well.

[pkgctrl]: https://sublime.wbond.net/

## Configuration
Configuration settings are stored in the user configuration file
(`Packages/User/Preferences.sublime-settings`). The following settings are
available:

* **extract_sublime_package_ask_on_open** -- if set to `true`, whenever you view
  a `.sublime-package` file in the editor, you will be asked if you want to
  extract the package. Defaults to `false`.

## About
Copyright (c) 2013 Felix Krull <f_krull@gmx.de>  
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1) Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2) Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3) The names of its contributors may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
