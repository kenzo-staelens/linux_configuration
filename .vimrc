set number
set list
set tabstop=4
set shiftwidth=4
set expandtab
highlight LineTooLong ctermbg=red guibg=red
highlight ExtraWhitespace ctermbg=red guibg=red
call matchadd("ExtraWhitespace",'\s\+$')
augroup silent! pygroup
" mark current position
"    autocmd BufWrite *.py :mark a
"    autocmd BufRead *.py :call matchadd("LineTooLong", '^.\{89,}$')
"    autocmd BufWrite *.py :retab
" comments have a space after #
"    autocmd BufWrite *.py silent! :%s/#\([^ ]\)/# \1/g
" remove blank lines at EOF
"    autocmd BufWrite *.py :%s/\($\n\s*\)*\%$//
" remove trailing whitespace
"    autocmd BufWrite *.py :%s/\s*$//g
" commas should be followed by a space, except for one element tuples
"    autocmd BufWrite *.py silent! :%s/\(.,\)\([^ )]\)/\1 \2/g
" top level items should be separated by two spaces
"    autocmd BufWrite *.py silent! :%s/^\(\s.\{-}$\)\(\n$\)*\n\([^ \}]\)/\1\r\r\r\3/g
" return to cursor
"    autocmd BufWrite *.py normal! `a
augroup END
