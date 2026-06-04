import sys

def main():
    path = 'src/components/NMCFormB.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add chunking variables
    chunk_vars = """
  const CLINICS_FIRST = 5;
  const CLINICS_CONT = 15;
  const clinicsChunks = useMemo(
    () => chunkArray(clinics, CLINICS_FIRST, CLINICS_CONT),
    [clinics]
  );
  const extraClinicsPages = Math.max(0, clinicsChunks.length - 1);
"""
    # Insert after `extraOtherHduEquipPages`
    insert_pos = content.find('const extraOtherHduEquipPages = Math.max(0, otherHduEquipChunks.length - 1);')
    if insert_pos != -1:
        end_line = content.find('\n', insert_pos)
        content = content[:end_line+1] + chunk_vars + content[end_line+1:]

    # Update pn function
    content = content.replace(
        'const pn = (base: number) => base + extraFacultyPages + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 7 ? extraHduEquipPages + extraOtherHduEquipPages : 0) + (base >= 10 ? extraPage9Pages : 0);',
        'const pn = (base: number) => base + extraFacultyPages + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 7 ? extraHduEquipPages + extraOtherHduEquipPages : 0) + (base >= 8 ? extraClinicsPages : 0) + (base >= 10 ? extraPage9Pages : 0);'
    )

    # 2. Modify Page 7 rendering
    page7_start = content.find('{/* PAGE 7 */}')
    page8_start = content.find('{/* PAGE 8+')

    page7_block = content[page7_start:page8_start]

    # Replace clinics map
    page7_block = page7_block.replace(
        'clinics.map(c =>',
        '(clinicsChunks[0] || []).map(c =>'
    )
    
    # Replace clinics Add button
    add_btn = '<button \n                className="no-print text-indigo-600 text-sm mb-4 flex items-center" \n                onClick={() => addRow(setClinics, () => ({ id: generateId(), name: \'\', days: \'\', timings: \'\', cases: \'\', incharge: \'\' }))}\n              >\n                <Plus className="w-4 h-4 mr-1"/> Add Record\n              </button>'
    new_add_btn = f'{{extraClinicsPages === 0 && ({add_btn})}}'
    page7_block = page7_block.replace(add_btn, new_add_btn)

    # 3. Create Continuation Pages
    cont_jsx = """
          {/* CONTINUATION PAGES: CLINICS */}
          {clinicsChunks.slice(1).map((chunk, ci) => (
            <div key={`clinics-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={7 + extraEquipPages + extraIcuEquipPages + extraOtherIcuEquipPages + extraHduEquipPages + extraOtherHduEquipPages + ci + 1} />
              <div className="pl-12 pr-4 w-full text-[10.5pt] mt-4">
                <p className="font-bold mb-2 flex"><span>Clinics: (Continued)</span></p>
                <table className="nmc-table tight-table text-[9pt] w-full mb-2">
                  <thead>
                    <tr><th className="w-40">Name of the Clinic</th><th className="w-24">Days</th><th className="w-24">Timings</th><th className="w-24">Average No. of<br/>cases per day</th><th>Name of Clinic In-charge</th><th className="w-10 no-print"></th></tr>
                  </thead>
                  <tbody>
                    {chunk.map(c => (
                      <tr key={c.id}>
                        <td><InlineInput value={c.name} onChange={(v:string)=>updateRow(setClinics, c.id, 'name', v)} /></td>
                        <td><InlineInput value={c.days} onChange={(v:string)=>updateRow(setClinics, c.id, 'days', v)} /></td>
                        <td><InlineInput value={c.timings} onChange={(v:string)=>updateRow(setClinics, c.id, 'timings', v)} /></td>
                        <td><InlineInput value={c.cases} onChange={(v:string)=>updateRow(setClinics, c.id, 'cases', v)} /></td>
                        <td><InlineInput value={c.incharge} onChange={(v:string)=>updateRow(setClinics, c.id, 'incharge', v)} /></td>
                        <td className="no-print text-center">
                          <button 
                            className="text-red-500 hover:text-red-700 p-1 flex items-center justify-center w-full h-full"
                            onClick={() => removeRow(setClinics, c.id)}
                            title="Delete Row"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {ci === extraClinicsPages - 1 && (
                  <button 
                    className="no-print text-indigo-600 text-sm mb-4 flex items-center" 
                    onClick={() => addRow(setClinics, () => ({ id: generateId(), name: '', days: '', timings: '', cases: '', incharge: '' }))}
                  >
                    <Plus className="w-4 h-4 mr-1"/> Add Record
                  </button>
                )}
              </div>
              <PageFooter />
            </div>
          ))}
"""

    page7_block = page7_block + cont_jsx
    content = content[:page7_start] + page7_block + content[page8_start:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Success")

if __name__ == '__main__':
    main()
