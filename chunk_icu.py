import sys

def main():
    path = 'src/components/NMCFormB.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add chunking variables
    chunk_vars = """
  const ICU_FIRST = 12;
  const ICU_CONT = 20;
  const icuEquipChunks = useMemo(
    () => chunkArray(icuEquips, ICU_FIRST, ICU_CONT),
    [icuEquips]
  );
  const extraIcuEquipPages = Math.max(0, icuEquipChunks.length - 1);

  const OTHER_ICU_FIRST = 4;
  const OTHER_ICU_CONT = 20;
  const otherIcuEquipChunks = useMemo(
    () => chunkArray(otherIcuEquips, OTHER_ICU_FIRST, OTHER_ICU_CONT),
    [otherIcuEquips]
  );
  const extraOtherIcuEquipPages = Math.max(0, otherIcuEquipChunks.length - 1);
"""
    # Insert after `extraEquipPages`
    insert_pos = content.find('const extraEquipPages = Math.max(0, equipChunks.length - 1);')
    if insert_pos != -1:
        end_line = content.find('\n', insert_pos)
        content = content[:end_line+1] + chunk_vars + content[end_line+1:]

    # Update pn function
    content = content.replace(
        'const pn = (base: number) => base + extraFacultyPages + (base >= 5 ? extraEquipPages : 0) + (base >= 10 ? extraPage9Pages : 0);',
        'const pn = (base: number) => base + extraFacultyPages + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 10 ? extraPage9Pages : 0);'
    )

    # 2. Modify Page 5 rendering
    page5_start = content.find('{/* PAGE 5 */}')
    page6_start = content.find('{/* PAGE 6 */}')

    page5_block = content[page5_start:page6_start]

    # Replace icuEquips map
    page5_block = page5_block.replace(
        'icuEquips.map((eq, idx) => {',
        '(icuEquipChunks[0] || []).map((eq, idx) => {'
    )
    
    # Replace otherIcuEquips map
    page5_block = page5_block.replace(
        'otherIcuEquips.map((eq, idx) => {',
        '(otherIcuEquipChunks[0] || []).map((eq, idx) => {'
    )
    
    # Replace otherIcuEquips Add button
    add_btn = '<button \n                  className="no-print text-indigo-600 text-sm mb-4 flex items-center" \n                  onClick={() => addRow(setOtherIcuEquips, () => ({ id: generateId(), item: \'\', num: \'\', available: \'\', functional: \'\', remarks: \'\' }))}\n                >\n                  <Plus className="w-4 h-4 mr-1"/> Add Record\n                </button>'
    new_add_btn = f'{{extraOtherIcuEquipPages === 0 && ({add_btn})}}'
    page5_block = page5_block.replace(add_btn, new_add_btn)

    # 3. Create Continuation Pages
    cont_jsx = """
          {/* CONTINUATION PAGES: ICU EQUIPS */}
          {icuEquipChunks.slice(1).map((chunk, ci) => (
            <div key={`icu-equip-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={5 + extraEquipPages + ci + 1} />
              <div className="pl-12 w-full text-[10.5pt] mt-4">
                <p className="font-bold mb-2 flex"><span className="w-8">i.</span><span>Equipment in ICU (Continued)</span></p>
                <table className="nmc-table tight-table text-[9pt] w-[95%] mb-4">
                  <thead>
                    <tr>
                      <th className="w-[35%]">Name of the item</th>
                      <th className="w-[12%]">Required</th>
                      <th className="w-[12%]">Available</th>
                      <th className="w-[12%]">Functional</th>
                      <th className="w-[29%]">Remarks</th>
                    </tr>
                  </thead>
                  <tbody>
                    {chunk.map((eq, idx) => (
                        <tr key={eq.id}>
                          <td><InlineTextarea value={eq.item} onChange={(v:string)=>updateRow(setIcuEquips, eq.id, 'item', v)} /></td>
                          <td><InlineTextarea value={eq.num} onChange={(v:string)=>updateRow(setIcuEquips, eq.id, 'num', v)} /></td>
                          <td><InlineSelect value={eq.available} onChange={(v:string)=>updateRow(setIcuEquips, eq.id, 'available', v)} options={["Available", "Not Available"]} /></td>
                          <td><InlineTextarea value={eq.functional} onChange={(v:string)=>updateRow(setIcuEquips, eq.id, 'functional', v)} /></td>
                          <td><InlineTextarea value={eq.remarks} onChange={(v:string)=>updateRow(setIcuEquips, eq.id, 'remarks', v)} /></td>
                        </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <PageFooter />
            </div>
          ))}

          {/* CONTINUATION PAGES: OTHER ICU EQUIPS */}
          {otherIcuEquipChunks.slice(1).map((chunk, ci) => (
            <div key={`other-icu-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={5 + extraEquipPages + extraIcuEquipPages + ci + 1} />
              <div className="pl-12 w-full text-[10.5pt] mt-4">
                <p className="font-bold mb-2 flex"><span>Other equipments for ICU: (Continued)</span></p>
                <table className="nmc-table tight-table text-[9pt] w-[95%] mb-2">
                  <thead>
                    <tr>
                      <th className="w-[35%]">Name of the item</th>
                      <th className="w-[12%]">Required</th>
                      <th className="w-[12%]">Available</th>
                      <th className="w-[12%]">Functional</th>
                      <th className="w-[29%]">Remarks</th>
                    </tr>
                  </thead>
                  <tbody>
                    {chunk.map((eq, idx) => (
                        <tr key={eq.id}>
                          <td><InlineTextarea value={eq.item} onChange={(v:string)=>updateRow(setOtherIcuEquips, eq.id, 'item', v)} /></td>
                          <td><InlineTextarea value={eq.num} onChange={(v:string)=>updateRow(setOtherIcuEquips, eq.id, 'num', v)} /></td>
                          <td><InlineSelect value={eq.available} onChange={(v:string)=>updateRow(setOtherIcuEquips, eq.id, 'available', v)} options={["Available", "Not Available"]} /></td>
                          <td><InlineTextarea value={eq.functional} onChange={(v:string)=>updateRow(setOtherIcuEquips, eq.id, 'functional', v)} /></td>
                          <td>
                            <div className="flex items-start gap-1">
                              <div className="flex-1">
                                <InlineTextarea value={eq.remarks} onChange={(v:string)=>updateRow(setOtherIcuEquips, eq.id, 'remarks', v)} />
                              </div>
                              <button 
                                className="no-print text-red-500 hover:text-red-700 p-1 flex items-center justify-center shrink-0"
                                onClick={() => removeRow(setOtherIcuEquips, eq.id)}
                                title="Delete Row"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                    ))}
                  </tbody>
                </table>
                {ci === extraOtherIcuEquipPages - 1 && (
                  <button 
                    className="no-print text-indigo-600 text-sm mb-4 flex items-center" 
                    onClick={() => addRow(setOtherIcuEquips, () => ({ id: generateId(), item: '', num: '', available: '', functional: '', remarks: '' }))}
                  >
                    <Plus className="w-4 h-4 mr-1"/> Add Record
                  </button>
                )}
              </div>
              <PageFooter />
            </div>
          ))}
"""

    page5_block = page5_block + cont_jsx
    content = content[:page5_start] + page5_block + content[page6_start:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Success")

if __name__ == '__main__':
    main()
