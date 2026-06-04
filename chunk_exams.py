import sys

def main():
    path = 'src/components/NMCFormB.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add chunking variables
    chunk_vars = """
  const EXAM_EXT_FIRST = 3;
  const EXAM_EXT_CONT = 12;
  const extExaminersChunks = useMemo(
    () => chunkArray(externalExaminers, EXAM_EXT_FIRST, EXAM_EXT_CONT),
    [externalExaminers]
  );
  const extraExtExaminersPages = Math.max(0, extExaminersChunks.length - 1);

  const EXAM_INT_FIRST = 4;
  const EXAM_INT_CONT = 12;
  const intExaminersChunks = useMemo(
    () => chunkArray(internalExaminers, EXAM_INT_FIRST, EXAM_INT_CONT),
    [internalExaminers]
  );
  const extraIntExaminersPages = Math.max(0, intExaminersChunks.length - 1);

  const EXAM_STUD_FIRST = 10;
  const EXAM_STUD_CONT = 20;
  const examStudentsChunks = useMemo(
    () => chunkArray(examStudents, EXAM_STUD_FIRST, EXAM_STUD_CONT),
    [examStudents]
  );
  const extraExamStudentsPages = Math.max(0, examStudentsChunks.length - 1);
"""
    # Insert after `extraClinicsPages`
    insert_pos = content.find('const extraClinicsPages = Math.max(0, clinicsChunks.length - 1);')
    if insert_pos != -1:
        end_line = content.find('\n', insert_pos)
        content = content[:end_line+1] + chunk_vars + content[end_line+1:]

    # Update pn function
    content = content.replace(
        'const pn = (base: number) => base + extraFacultyPages + (base >= 2 ? extraPgInspPages : 0) + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 7 ? extraHduEquipPages + extraOtherHduEquipPages : 0) + (base >= 8 ? extraClinicsPages : 0) + (base >= 10 ? extraPage9Pages : 0);',
        'const pn = (base: number) => base + extraFacultyPages + (base >= 2 ? extraPgInspPages : 0) + (base >= 5 ? extraEquipPages : 0) + (base >= 6 ? extraIcuEquipPages + extraOtherIcuEquipPages : 0) + (base >= 7 ? extraHduEquipPages + extraOtherHduEquipPages : 0) + (base >= 8 ? extraClinicsPages : 0) + (base >= 10 ? extraPage9Pages : 0) + (base >= 12 ? extraExtExaminersPages + extraIntExaminersPages + extraExamStudentsPages : 0);'
    )

    # 2. Modify Page 11 rendering
    page11_start = content.find('{/* PAGE 11 */}')
    page12_start = content.find('{/* PAGE 12 */}')

    page11_block = content[page11_start:page12_start]

    # Replace maps
    page11_block = page11_block.replace(
        'externalExaminers.map(ex =>',
        '(extExaminersChunks[0] || []).map(ex =>'
    )
    page11_block = page11_block.replace(
        'internalExaminers.map(ex =>',
        '(intExaminersChunks[0] || []).map(ex =>'
    )
    page11_block = page11_block.replace(
        'examStudents.map(s =>',
        '(examStudentsChunks[0] || []).map(s =>'
    )
    
    # Replace Add buttons
    add_btn1 = '<button \n                className="no-print text-indigo-600 text-sm mb-4 flex items-center" \n                onClick={() => addRow(setExternalExaminers, () => ({ id: generateId(), name: \'\', designation: \'\', institution: \'\', email: \'\', mobile: \'\' }))}\n              >\n                <Plus className="w-4 h-4 mr-1"/> Add Record\n              </button>'
    page11_block = page11_block.replace(add_btn1, f'{{extraExtExaminersPages === 0 && ({add_btn1})}}')

    add_btn2 = '<button \n                className="no-print text-indigo-600 text-sm mb-4 flex items-center" \n                onClick={() => addRow(setInternalExaminers, () => ({ id: generateId(), name: \'\', designation: \'\', email: \'\', mobile: \'\' }))}\n              >\n                <Plus className="w-4 h-4 mr-1"/> Add Record\n              </button>'
    page11_block = page11_block.replace(add_btn2, f'{{extraIntExaminersPages === 0 && ({add_btn2})}}')

    add_btn3 = '<button \n                className="no-print text-indigo-600 text-sm mb-4 flex items-center" \n                onClick={() => addRow(setExamStudents, () => ({ id: generateId(), name: \'\', passFail: \'\' }))}\n              >\n                <Plus className="w-4 h-4 mr-1"/> Add Record\n              </button>'
    page11_block = page11_block.replace(add_btn3, f'{{extraExamStudentsPages === 0 && ({add_btn3})}}')

    # 3. Create Continuation Pages
    cont_jsx = """
          {/* CONTINUATION PAGES: EXAM */}
          {extExaminersChunks.slice(1).map((chunk, ci) => (
            <div key={`ext-exam-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={pn(11) + ci + 1} />
              <div className="pl-8 pr-4 w-full mt-4 text-[10.5pt]">
                <p className="font-bold mb-2 flex"><span>External Examiners: (Continued)</span></p>
                <table className="nmc-table tight-table text-[10pt] border-t-0 mb-4 w-full">
                  <thead>
                    <tr><th className="w-48">Name</th><th className="w-32">Designation</th><th className="w-48">Institution</th><th>E-mail</th><th className="w-24">Mobile no</th><th className="w-10 no-print"></th></tr>
                  </thead>
                  <tbody>
                    {chunk.map(ex => (
                      <tr key={ex.id}>
                        <td><InlineInput value={ex.name} onChange={(v:string)=>updateRow(setExternalExaminers, ex.id, 'name', v)} /></td>
                        <td><InlineInput value={ex.designation} onChange={(v:string)=>updateRow(setExternalExaminers, ex.id, 'designation', v)} /></td>
                        <td><InlineInput value={ex.institution} onChange={(v:string)=>updateRow(setExternalExaminers, ex.id, 'institution', v)} /></td>
                        <td><InlineInput value={ex.email} onChange={(v:string)=>updateRow(setExternalExaminers, ex.id, 'email', v)} /></td>
                        <td><InlineInput value={ex.mobile} onChange={(v:string)=>updateRow(setExternalExaminers, ex.id, 'mobile', v)} /></td>
                        <td className="no-print text-center"><button className="text-red-500 hover:text-red-700 p-1" onClick={() => removeRow(setExternalExaminers, ex.id)}><Trash2 className="w-4 h-4" /></button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {ci === extraExtExaminersPages - 1 && (
                  <button className="no-print text-indigo-600 text-sm mb-4 flex items-center" onClick={() => addRow(setExternalExaminers, () => ({ id: generateId(), name: '', designation: '', institution: '', email: '', mobile: '' }))}><Plus className="w-4 h-4 mr-1"/> Add Record</button>
                )}
              </div>
              <PageFooter />
            </div>
          ))}

          {intExaminersChunks.slice(1).map((chunk, ci) => (
            <div key={`int-exam-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={pn(11) + extraExtExaminersPages + ci + 1} />
              <div className="pl-8 pr-4 w-full mt-4 text-[10.5pt]">
                <p className="font-bold mb-2 flex"><span>Internal Examiners: (Continued)</span></p>
                <table className="nmc-table tight-table text-[10pt] mb-4 w-[85%]">
                  <thead>
                    <tr><th className="w-48">Name</th><th className="w-32">Designation</th><th>E-mail</th><th className="w-24">Mobile no</th><th className="w-10 no-print"></th></tr>
                  </thead>
                  <tbody>
                    {chunk.map(ex => (
                      <tr key={ex.id}>
                        <td><InlineInput value={ex.name} onChange={(v:string)=>updateRow(setInternalExaminers, ex.id, 'name', v)} /></td>
                        <td><InlineInput value={ex.designation} onChange={(v:string)=>updateRow(setInternalExaminers, ex.id, 'designation', v)} /></td>
                        <td><InlineInput value={ex.email} onChange={(v:string)=>updateRow(setInternalExaminers, ex.id, 'email', v)} /></td>
                        <td><InlineInput value={ex.mobile} onChange={(v:string)=>updateRow(setInternalExaminers, ex.id, 'mobile', v)} /></td>
                        <td className="no-print text-center"><button className="text-red-500 hover:text-red-700 p-1" onClick={() => removeRow(setInternalExaminers, ex.id)}><Trash2 className="w-4 h-4" /></button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {ci === extraIntExaminersPages - 1 && (
                  <button className="no-print text-indigo-600 text-sm mb-4 flex items-center" onClick={() => addRow(setInternalExaminers, () => ({ id: generateId(), name: '', designation: '', email: '', mobile: '' }))}><Plus className="w-4 h-4 mr-1"/> Add Record</button>
                )}
              </div>
              <PageFooter />
            </div>
          ))}

          {examStudentsChunks.slice(1).map((chunk, ci) => (
            <div key={`exam-stud-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={pn(11) + extraExtExaminersPages + extraIntExaminersPages + ci + 1} />
              <div className="pl-8 pr-4 w-full mt-4 text-[10.5pt]">
                <p className="font-bold mb-2 flex"><span>Details of Examinees: (Continued)</span></p>
                <table className="nmc-table tight-table text-[10pt] mb-4 w-[60%]">
                  <thead>
                    <tr><th className="w-16">Sr No</th><th>Name of student</th><th className="w-32">Pass / Fail</th><th className="w-10 no-print"></th></tr>
                  </thead>
                  <tbody>
                    {chunk.map((s, idx) => (
                      <tr key={s.id}>
                        <td className="text-center">{EXAM_STUD_FIRST + ci * EXAM_STUD_CONT + idx + 1}</td>
                        <td><InlineInput value={s.name} onChange={(v:string)=>updateRow(setExamStudents, s.id, 'name', v)} /></td>
                        <td><InlineSelect value={s.passFail} onChange={(v:string)=>updateRow(setExamStudents, s.id, 'passFail', v)} options={["Pass", "Fail"]} /></td>
                        <td className="no-print text-center"><button className="text-red-500 hover:text-red-700 p-1" onClick={() => removeRow(setExamStudents, s.id)}><Trash2 className="w-4 h-4" /></button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {ci === extraExamStudentsPages - 1 && (
                  <button className="no-print text-indigo-600 text-sm mb-4 flex items-center" onClick={() => addRow(setExamStudents, () => ({ id: generateId(), name: '', passFail: '' }))}><Plus className="w-4 h-4 mr-1"/> Add Record</button>
                )}
              </div>
              <PageFooter />
            </div>
          ))}
"""

    page11_block = page11_block + cont_jsx
    content = content[:page11_start] + page11_block + content[page12_start:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Success")

if __name__ == '__main__':
    main()
