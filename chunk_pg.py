import sys

def main():
    path = 'src/components/NMCFormB.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add chunking variables
    chunk_vars = """
  const PG_INSP_FIRST = 3;
  const PG_INSP_CONT = 12;
  const pgInspChunks = useMemo(
    () => chunkArray(pgInspections, PG_INSP_FIRST, PG_INSP_CONT),
    [pgInspections]
  );
  const extraPgInspPages = Math.max(0, pgInspChunks.length - 1);
"""
    # Insert before `extraEquipPages` (doesn't matter where exactly, let's put it right after pgInspections definition, no wait, the chunk vars must be after all states)
    insert_pos = content.find('const equipChunks = useMemo(')
    if insert_pos != -1:
        # find start of line
        start_line = content.rfind('\n', 0, insert_pos)
        content = content[:start_line+1] + chunk_vars + content[start_line+1:]

    # Update pn function
    content = content.replace(
        'const pn = (base: number) => base + extraFacultyPages + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 7 ? extraHduEquipPages + extraOtherHduEquipPages : 0) + (base >= 8 ? extraClinicsPages : 0) + (base >= 10 ? extraPage9Pages : 0);',
        'const pn = (base: number) => base + extraFacultyPages + (base >= 2 ? extraPgInspPages : 0) + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 7 ? extraHduEquipPages + extraOtherHduEquipPages : 0) + (base >= 8 ? extraClinicsPages : 0) + (base >= 10 ? extraPage9Pages : 0);'
    )

    # 2. Modify Page 1 rendering
    page1_start = content.find('{/* PAGE 1 */}')
    page2_start = content.find('{/* PAGE 2 */}')

    page1_block = content[page1_start:page2_start]

    # Replace map
    page1_block = page1_block.replace(
        '{pgInspections.map(insp => (',
        '{pgInspChunks[0]?.map(insp => ('
    )
    
    # Replace Add button
    add_btn = '<button className="no-print text-indigo-600 text-sm mb-2 flex items-center" onClick={()=>addRow(setPgInspections, ()=>({id:generateId(), date:\'\', purpose:\'\', type:\'\', outcome:\'\', seatsInc:\'\', seatsDec:\'\', order:\'\'}))}><Plus className="w-4 h-4 mr-1"/> Add Record</button>'
    new_add_btn = f'{{extraPgInspPages === 0 && ({add_btn})}}'
    page1_block = page1_block.replace(add_btn, new_add_btn)

    # 3. Create Continuation Pages
    cont_jsx = """
            {/* CONTINUATION PAGES: PG INSPECTIONS */}
            {pgInspChunks.slice(1).map((chunk, ci) => (
              <div key={`pg-insp-cont-${ci}`} className="a4-page portrait-page print-page">
                <PageHeader pageNum={1 + ci + 1} />
                <div className="pl-4 mt-4">
                  <div className="flex items-end mb-1">
                    <span className="w-8">i.</span>
                    <span className="mr-2 whitespace-nowrap font-bold">Details of PG inspections of the department in last five years: (Continued)</span>
                  </div>
                  <table className="nmc-table tight-table text-[8.5pt] leading-[1.2] w-full">
                    <thead>
                      <tr>
                        <th className="w-[10%]">Date of<br/>Inspection</th>
                        <th className="w-[24%]">Purpose of<br/>Inspection<br/><span className="font-normal italic">(LoP for starting a course/permission for increase of seats/ Recognition of course/ Recognition of increased seats /Renewal of Recognition/Surprise /Random Inspection/ Compliance Verification inspection/other)</span></th>
                        <th className="w-[12%]">Type of<br/>Inspection<br/><span className="font-normal">(Physical/<br/>Virtual)</span></th>
                        <th className="w-[24%]">Outcome<br/><span className="font-normal italic">(LoP received/denied. Permission for increase of seats received/denied. Recognition of course done/denied. Recognition of increased seats done/denied /Renewal of Recognition done/denied /other)</span></th>
                        <th className="w-[8%]">No of seats<br/>Increased</th>
                        <th className="w-[8%]">No of seats<br/>Decreased</th>
                        <th className="w-[14%]">Order issued<br/>on the basis of<br/>inspection<br/><span className="font-normal italic">(Attach copy of all the order issued by NMC/MCI) as Annexure</span></th>
                        <th className="w-10 no-print"></th>
                      </tr>
                    </thead>
                    <tbody>
                      {chunk.map(insp => (
                        <tr key={insp.id}>
                          <td><InlineTextarea value={insp.date} onChange={(v:string)=>updateRow(setPgInspections, insp.id, 'date', v)} /></td>
                          <td><InlineTextarea value={insp.purpose} onChange={(v:string)=>updateRow(setPgInspections, insp.id, 'purpose', v)} /></td>
                          <td><InlineTextarea value={insp.type} onChange={(v:string)=>updateRow(setPgInspections, insp.id, 'type', v)} /></td>
                          <td><InlineTextarea value={insp.outcome} onChange={(v:string)=>updateRow(setPgInspections, insp.id, 'outcome', v)} /></td>
                          <td><InlineInput value={insp.seatsInc} onChange={(v:string)=>updateRow(setPgInspections, insp.id, 'seatsInc', v)} /></td>
                          <td><InlineInput value={insp.seatsDec} onChange={(v:string)=>updateRow(setPgInspections, insp.id, 'seatsDec', v)} /></td>
                          <td><InlineTextarea value={insp.order} onChange={(v:string)=>updateRow(setPgInspections, insp.id, 'order', v)} /></td>
                          <td className="no-print text-center">
                            <button 
                              className="text-red-500 hover:text-red-700 p-1 flex items-center justify-center w-full h-full"
                              onClick={() => removeRow(setPgInspections, insp.id)}
                              title="Delete Row"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {ci === extraPgInspPages - 1 && (
                    <button className="no-print text-indigo-600 text-sm mb-2 flex items-center" onClick={()=>addRow(setPgInspections, ()=>({id:generateId(), date:'', purpose:'', type:'', outcome:'', seatsInc:'', seatsDec:'', order:''}))}><Plus className="w-4 h-4 mr-1"/> Add Record</button>
                  )}
                </div>
                <PageFooter />
              </div>
            ))}
"""

    page1_block = page1_block + cont_jsx
    content = content[:page1_start] + page1_block + content[page2_start:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Success")

if __name__ == '__main__':
    main()
