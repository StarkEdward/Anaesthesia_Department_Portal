import sys

def main():
    path = 'src/components/NMCFormB.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add chunking variables
    chunk_vars = """
  const HDU_FIRST = 12;
  const HDU_CONT = 20;
  const hduEquipChunks = useMemo(
    () => chunkArray(hduEquips, HDU_FIRST, HDU_CONT),
    [hduEquips]
  );
  const extraHduEquipPages = Math.max(0, hduEquipChunks.length - 1);

  const OTHER_HDU_FIRST = 4;
  const OTHER_HDU_CONT = 20;
  const otherHduEquipChunks = useMemo(
    () => chunkArray(otherHduEquips, OTHER_HDU_FIRST, OTHER_HDU_CONT),
    [otherHduEquips]
  );
  const extraOtherHduEquipPages = Math.max(0, otherHduEquipChunks.length - 1);
"""
    # Insert after `extraOtherIcuEquipPages`
    insert_pos = content.find('const extraOtherIcuEquipPages = Math.max(0, otherIcuEquipChunks.length - 1);')
    if insert_pos != -1:
        end_line = content.find('\n', insert_pos)
        content = content[:end_line+1] + chunk_vars + content[end_line+1:]

    # Update pn function
    content = content.replace(
        'const pn = (base: number) => base + extraFacultyPages + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 10 ? extraPage9Pages : 0);',
        'const pn = (base: number) => base + extraFacultyPages + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 7 ? extraHduEquipPages + extraOtherHduEquipPages : 0) + (base >= 10 ? extraPage9Pages : 0);'
    )

    # 2. Modify Page 6 rendering
    page6_start = content.find('{/* PAGE 6 */}')
    page7_start = content.find('{/* PAGE 7 */}')

    page6_block = content[page6_start:page7_start]

    # Replace hduEquips map
    page6_block = page6_block.replace(
        'hduEquips.map((eq, idx) => {',
        '(hduEquipChunks[0] || []).map((eq, idx) => {'
    )
    
    # Replace otherHduEquips map
    page6_block = page6_block.replace(
        'otherHduEquips.map((eq, idx) => {',
        '(otherHduEquipChunks[0] || []).map((eq, idx) => {'
    )
    
    # Replace otherHduEquips Add button
    add_btn = '<button \n                  className="no-print text-indigo-600 text-sm mb-4 flex items-center" \n                  onClick={() => addRow(setOtherHduEquips, () => ({ id: generateId(), item: \'\', num: \'\', available: \'\', functional: \'\', remarks: \'\' }))}\n                >\n                  <Plus className="w-4 h-4 mr-1"/> Add Record\n                </button>'
    new_add_btn = f'{{extraOtherHduEquipPages === 0 && ({add_btn})}}'
    page6_block = page6_block.replace(add_btn, new_add_btn)

    # 3. Create Continuation Pages
    cont_jsx = """
          {/* CONTINUATION PAGES: HDU EQUIPS */}
          {hduEquipChunks.slice(1).map((chunk, ci) => (
            <div key={`hdu-equip-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={6 + extraEquipPages + extraIcuEquipPages + extraOtherIcuEquipPages + ci + 1} />
              <div className="pl-12 pr-4 w-full text-[10.5pt] mt-4 space-y-4">
                <p className="font-bold mb-2 flex"><span className="w-8">ii.</span><span>Equipment in HDU (Continued)</span></p>
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
                          <td><InlineTextarea value={eq.item} onChange={(v:string)=>updateRow(setHduEquips, eq.id, 'item', v)} /></td>
                          <td><InlineTextarea value={eq.num} onChange={(v:string)=>updateRow(setHduEquips, eq.id, 'num', v)} /></td>
                          <td><InlineSelect value={eq.available} onChange={(v:string)=>updateRow(setHduEquips, eq.id, 'available', v)} options={["Available", "Not Available"]} /></td>
                          <td><InlineTextarea value={eq.functional} onChange={(v:string)=>updateRow(setHduEquips, eq.id, 'functional', v)} /></td>
                          <td><InlineTextarea value={eq.remarks} onChange={(v:string)=>updateRow(setHduEquips, eq.id, 'remarks', v)} /></td>
                        </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <PageFooter />
            </div>
          ))}

          {/* CONTINUATION PAGES: OTHER HDU EQUIPS */}
          {otherHduEquipChunks.slice(1).map((chunk, ci) => (
            <div key={`other-hdu-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={6 + extraEquipPages + extraIcuEquipPages + extraOtherIcuEquipPages + extraHduEquipPages + ci + 1} />
              <div className="pl-12 pr-4 w-full text-[10.5pt] mt-4 space-y-4">
                <p className="font-bold mb-2 flex"><span>Other equipments for HDU: (Continued)</span></p>
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
                          <td><InlineTextarea value={eq.item} onChange={(v:string)=>updateRow(setOtherHduEquips, eq.id, 'item', v)} /></td>
                          <td><InlineTextarea value={eq.num} onChange={(v:string)=>updateRow(setOtherHduEquips, eq.id, 'num', v)} /></td>
                          <td><InlineSelect value={eq.available} onChange={(v:string)=>updateRow(setOtherHduEquips, eq.id, 'available', v)} options={["Available", "Not Available"]} /></td>
                          <td><InlineTextarea value={eq.functional} onChange={(v:string)=>updateRow(setOtherHduEquips, eq.id, 'functional', v)} /></td>
                          <td>
                            <div className="flex items-start gap-1">
                              <div className="flex-1">
                                <InlineTextarea value={eq.remarks} onChange={(v:string)=>updateRow(setOtherHduEquips, eq.id, 'remarks', v)} />
                              </div>
                              <button 
                                className="no-print text-red-500 hover:text-red-700 p-1 flex items-center justify-center shrink-0"
                                onClick={() => removeRow(setOtherHduEquips, eq.id)}
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
                {ci === extraOtherHduEquipPages - 1 && (
                  <button 
                    className="no-print text-indigo-600 text-sm mb-4 flex items-center" 
                    onClick={() => addRow(setOtherHduEquips, () => ({ id: generateId(), item: '', num: '', available: '', functional: '', remarks: '' }))}
                  >
                    <Plus className="w-4 h-4 mr-1"/> Add Record
                  </button>
                )}
              </div>
              <PageFooter />
            </div>
          ))}
"""

    page6_block = page6_block + cont_jsx
    content = content[:page6_start] + page6_block + content[page7_start:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Success")

if __name__ == '__main__':
    main()
