from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/box64/src/elfs/elfloader.c")
text = path.read_text(encoding="utf-8")
old = """            if(e->p_filesz) {
                fseeko(head->file, e->p_offset, SEEK_SET);
                if(fread(dest, e->p_filesz, 1, head->file)!=1) {
                    mutex_unlock(&context->mutex_tls);
                    printf_log(LOG_NONE, "Fail to read PT_TLS part #%zu (size=%zd)\\n", i, e->p_filesz);
                    return 1;
                }
            }
"""
new = """            if(e->p_filesz) {
                int tls_ok = (fseeko(head->file, e->p_offset, SEEK_SET)==0 && fread(dest, e->p_filesz, 1, head->file)==1);
                if(!tls_ok) {
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
                    tls_ok = (tls_off >= 0 && fseeko(head->file, tls_off, SEEK_SET)==0 && fread(dest, e->p_filesz, 1, head->file)==1);
                }
                if(!tls_ok) {
                    mutex_unlock(&context->mutex_tls);
                    printf_log(LOG_NONE, "Fail to read PT_TLS part #%zu (size=%zd)\\n", i, e->p_filesz);
                    return 1;
                }
            }
"""
count = text.count(old)
if count != 1:
    raise SystemExit(f"trecho do TLS encontrado {count} vezes")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("box64 TLS fallback aplicado")
