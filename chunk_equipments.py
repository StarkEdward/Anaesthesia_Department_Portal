import sys

def main():
    path = 'src/components/NMCFormB.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add chunking variables
    chunk_vars = """
  const EQUIP_FIRST = 15;
  const EQUIP_CONT = 20;
  const equipChunks = useMemo(
    () => chunkArray(equipments, EQUIP_FIRST, EQUIP_CONT),
    [equipments]
  );
  const extraEquipPages = Math.max(0, equipChunks.length - 1);
"""
    # Insert after `extraPage9Pages`
    insert_pos = content.find('const extraPage9Pages = extraEligiblePages + extraPgStudyingPages + extraPastPgPages;')
    if insert_pos != -1:
        # find end of line
        end_line = content.find('\n', insert_pos)
        content = content[:end_line+1] + chunk_vars + content[end_line+1:]

    # Update pn function
    content = content.replace(
        'const pn = (base: number) => base + extraFacultyPages + (base >= 10 ? extraPage9Pages : 0);',
        'const pn = (base: number) => base + extraFacultyPages + (base >= 5 ? extraEquipPages : 0) + (base >= 10 ? extraPage9Pages : 0);'
    )

    # 2. Modify Page 4 rendering
    # Find Page 4 start
    page4_start = content.find('{/* PAGE 4 */}')
    page5_start = content.find('{/* PAGE 5 */}')

    page4_block = content[page4_start:page5_start]

    page4_block = page4_block.replace(
        'equipments.map((eq, idx) => {',
        '(equipChunks[0] || []).map((eq, idx) => {'
    )
    
    add_btn = '<button className="no-print text-indigo-600 text-sm mb-2 ml-4 flex items-center" onClick={()=>addRow(setEquipments, ()=>({id:generateId(), name:\'\', available:\'\', functional:\'\', specs:\'\', adequate:\'\'}))}><Plus className="w-4 h-4 mr-1"/> Add Record</button>'
    new_add_btn = f'{{extraEquipPages === 0 && ({add_btn})}}'
    page4_block = page4_block.replace(add_btn, new_add_btn)

    # 3. Create Continuation Pages
    cont_jsx = """
          {/* CONTINUATION PAGES: EQUIPMENTS */}
          {equipChunks.slice(1).map((chunk, ci) => (
            <div key={`equip-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={4 + ci + 1} />
              <div className="pl-8 mt-4 text-[10.5pt]">
                <p className="font-bold mb-2 flex"><span className="w-8">g.</span><span>Equipment: (Continued)</span></p>
                <table className="nmc-table tight-table text-[9.5pt] w-[95%] ml-4">
                  <thead>
                    <tr>
                      <th className="w-[26%]">Equipment name</th>
                      <th className="w-[16%]">Numbers<br/>available</th>
                      <th className="w-[14%]">Functional<br/>status</th>
                      <th className="w-[32%]">Important<br/>Specification in Brief</th>
                      <th className="w-[12%]">Adequate<br/>Yes/No</th>
                    </tr>
                  </thead>
                  <tbody>
                    {chunk.map((eq, idx) => {
                      const isStandard = false; // Cont pages only have custom items
                      return (
                        <tr key={eq.id}>
                          <td>
                            <InlineTextarea value={eq.name} onChange={(v:string)=>updateRow(setEquipments, eq.id, 'name', v)} />
                          </td>
                          <td><InlineTextarea value={eq.available} onChange={(v:string)=>updateRow(setEquipments, eq.id, 'available', v)} /></td>
                          <td><InlineTextarea value={eq.functional} onChange={(v:string)=>updateRow(setEquipments, eq.id, 'functional', v)} /></td>
                          <td><InlineTextarea value={eq.specs} onChange={(v:string)=>updateRow(setEquipments, eq.id, 'specs', v)} /></td>
                          <td>
                            <div className="flex items-center gap-1">
                              <div className="flex-1">
                                <InlineSelect value={eq.adequate} onChange={(v:string)=>updateRow(setEquipments, eq.id, 'adequate', v)} options={["Yes", "No"]} />
                              </div>
                              <button 
                                className="no-print text-red-500 hover:text-red-700 p-1 flex items-center justify-center shrink-0"
                                onClick={() => removeRow(setEquipments, eq.id)}
                                title="Delete Row"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
                {ci === extraEquipPages - 1 && (
                  <button className="no-print text-indigo-600 text-sm mb-2 ml-4 mt-2 flex items-center" onClick={()=>addRow(setEquipments, ()=>({id:generateId(), name:'', available:'', functional:'', specs:'', adequate:''}))}><Plus className="w-4 h-4 mr-1"/> Add Record</button>
                )}
              </div>
              <PageFooter />
            </div>
          ))}
"""

    page4_block = page4_block + cont_jsx
    content = content[:page4_start] + page4_block + content[page5_start:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Success")

if __name__ == '__main__':
    main()
