from pathlib import Path

path = Path("/tmp/box64/src/elfs/elfloader.c")
text = path.read_text()
marker = "Fail to read PT_TLS part #%zu (size=%zd)\\n"
at = text.find("Fail to read PT_TLS")
if at < 0:
    raise SystemExit("ponto do TLS nao encontrado")
start = text.rfind("if(e->p_filesz)", 0, at)
end = text.find("\n", text.find("return 1;", at))
if start < 0 or end < 0:
    raise SystemExit("bloco do TLS incompleto")
end = text.find("\n", end) + 1
# include the closing brace of if(e->p_filesz)
brace = text.find("}", end)
end = text.find("\n", brace) + 1
replacement = """if(e->p_filesz) {
            if(fseeko(head->file, e->p_offset, SEEK_SET)!=0 || fread(dest, e->p_filesz, 1, head->file)!=1) {
                off_t tls_off = -1;
                for(size_t j = 0; j < head->numPHEntries; ++j) {
                    Elf64_Phdr *load = &head->PHEntries._64[j];
                    if(load->p_type==PT_LOAD && load->p_filesz
                        && load->p_vaddr <= e->p_vaddr
                        && e->p_vaddr + e->p_filesz <= load->p_vaddr + load->p_filesz) {
                        tls_off = (off_t)(load->p_offset + (e->p_vaddr - load->p_vaddr));
                        break;
                    }
                }
                if(tls_off < 0 || fseeko(head->file, tls_off, SEEK_SET)!=0 || fread(dest, e->p_filesz, 1, head->file)!=1) {
                    mutex_unlock(&context->mutex_tls);
                    printf_log(LOG_NONE, "Fail to read PT_TLS part #%zu (size=%zd)\\n", i, e->p_filesz);
                    return 1;
                }
            }
        }
"""
text = text[:start] + replacement + text[end:]
path.write_text(text)
print("box64 TLS fallback aplicado")
