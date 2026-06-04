import re
import sys

def main():
    path = 'src/components/NMCFormB.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where PAGE 9 starts
    page9_idx = content.find('{/* PAGE 9+offset */}')
    if page9_idx == -1:
        print("Could not find PAGE 9+offset")
        return

    # Find where PAGE 11 starts (which is the next main page comment)
    page11_idx = content.find('{/* PAGE 11 */}', page9_idx)
    if page11_idx == -1:
        print("Could not find PAGE 11")
        return

    page_9_block = content[page9_idx:page11_idx]

    # Now we need to modify the blocks inside page_9_block
    # We will replace `eligibleFaculties.map` with `eligibleFacChunks[0]?.map`
    # and `pgStudents.map` with `pgStudyingChunks[0]?.map`
    # and `pastPgStudents.map` with `pastPgChunks[0]?.map`

    # Actually, it's safer to just do simple replacements on the whole block:
    # 1. eligibleFaculties
    block_mod = page_9_block.replace(
        'eligibleFaculties.map((f, i)',
        '(eligibleFacChunks[0] || []).map((f, i)'
    )
    block_mod = block_mod.replace(
        'eligibleFaculties.length',
        '(eligibleFacChunks[0] || []).length'
    )
    # The Add record button for faculties:
    block_mod = block_mod.replace(
        '<div className="no-print flex gap-3 mt-2 ml-8 mb-8 items-center">\n              <button\n                className="text-indigo-600 hover:text-indigo-800 text-sm flex items-center"\n                onClick={() => setEligibleFaculties(prev => [...prev, { id: generateId(), designation: \'\', num: \'\', name: \'\', seats: \'\', adequate: \'\' }])}\n              >\n                <Plus className="w-4 h-4 mr-1"/> Add Record\n              </button>\n            </div>',
        '{extraEligiblePages === 0 && (\n              <div className="no-print flex gap-3 mt-2 ml-8 mb-8 items-center">\n                <button\n                  className="text-indigo-600 hover:text-indigo-800 text-sm flex items-center"\n                  onClick={() => setEligibleFaculties(prev => [...prev, { id: generateId(), designation: \'\', num: \'\', name: \'\', seats: \'\', adequate: \'\' }])}\n                >\n                  <Plus className="w-4 h-4 mr-1"/> Add Record\n                </button>\n              </div>\n            )}'
    )

    # 2. pgStudents
    block_mod = block_mod.replace(
        'pgStudents.map(s =>',
        '(pgStudyingChunks[0] || []).map(s =>'
    )
    block_mod = block_mod.replace(
        '<div className="flex items-center gap-4 mb-6 ml-8 mt-2">\n              <button className="no-print text-indigo-600 text-sm flex items-center" onClick={()=>addRow(setPgStudents, ()=>({id:generateId(), name:\'\', joiningDate:\'\', phone:\'\', email:\'\'}))}>\n                <Plus className="w-4 h-4 mr-1"/> Add Record\n              </button>\n              <button className="no-print text-emerald-600 text-sm flex items-center border border-emerald-300 rounded px-2 py-0.5" onClick={() => { setDoctorSearch(\'\'); setSelectedDoctorIds(new Set()); setImportTarget(\'pgStudying\'); }}>\n                <Users className="w-4 h-4 mr-1"/> Import from Doctors\n              </button>\n            </div>',
        '{extraPgStudyingPages === 0 && (\n              <div className="flex items-center gap-4 mb-6 ml-8 mt-2">\n                <button className="no-print text-indigo-600 text-sm flex items-center" onClick={()=>addRow(setPgStudents, ()=>({id:generateId(), name:\'\', joiningDate:\'\', phone:\'\', email:\'\'}))}>\n                  <Plus className="w-4 h-4 mr-1"/> Add Record\n                </button>\n                <button className="no-print text-emerald-600 text-sm flex items-center border border-emerald-300 rounded px-2 py-0.5" onClick={() => { setDoctorSearch(\'\'); setSelectedDoctorIds(new Set()); setImportTarget(\'pgStudying\'); }}>\n                  <Users className="w-4 h-4 mr-1"/> Import from Doctors\n                </button>\n              </div>\n            )}'
    )

    # 3. pastPgStudents
    block_mod = block_mod.replace(
        'pastPgStudents.map(s =>',
        '(pastPgChunks[0] || []).map(s =>'
    )
    block_mod = block_mod.replace(
        '<div className="flex items-center gap-4 mb-8 ml-8 mt-2">\n              <button className="no-print text-indigo-600 text-sm flex items-center" onClick={()=>addRow(setPastPgStudents, ()=>({id:generateId(), name:\'\', joiningDate:\'\', relievingDate:\'\', phone:\'\', email:\'\'}))}>\n                <Plus className="w-4 h-4 mr-1"/> Add Record\n              </button>\n              <button className="no-print text-emerald-600 text-sm flex items-center border border-emerald-300 rounded px-2 py-0.5" onClick={() => { setDoctorSearch(\'\'); setSelectedDoctorIds(new Set()); setImportTarget(\'pgCompleted\'); }}>\n                <Users className="w-4 h-4 mr-1"/> Import from Doctors\n              </button>\n            </div>',
        '{extraPastPgPages === 0 && (\n              <div className="flex items-center gap-4 mb-8 ml-8 mt-2">\n                <button className="no-print text-indigo-600 text-sm flex items-center" onClick={()=>addRow(setPastPgStudents, ()=>({id:generateId(), name:\'\', joiningDate:\'\', relievingDate:\'\', phone:\'\', email:\'\'}))}>\n                  <Plus className="w-4 h-4 mr-1"/> Add Record\n                </button>\n                <button className="no-print text-emerald-600 text-sm flex items-center border border-emerald-300 rounded px-2 py-0.5" onClick={() => { setDoctorSearch(\'\'); setSelectedDoctorIds(new Set()); setImportTarget(\'pgCompleted\'); }}>\n                  <Users className="w-4 h-4 mr-1"/> Import from Doctors\n                </button>\n              </div>\n            )}'
    )

    # Now we need to append the Continuation Pages code directly AFTER this block (so before PAGE 11)
    
    continuation_jsx = """
          {/* CONTINUATION PAGES: ELIGIBLE FACULTIES */}
          {eligibleFacChunks.slice(1).map((chunk, ci) => (
            <div key={`ef-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={pn(9) + ci + 1} />
              <p className="font-bold mb-4 flex pl-8 pr-4 mt-4">
                <span className="w-8">ii.</span>
                <span className="text-justify">Total eligible faculties and Senior Residents... (Continued)</span>
              </p>
              <table className="nmc-table tight-table text-[10pt] ml-8 w-[92%] mb-8">
                <thead>
                  <tr>
                    <th className="w-32 text-left pl-2">Designation</th>
                    <th className="w-20 text-left pl-2">Number</th>
                    <th className="w-48 text-left pl-2">Name</th>
                    <th className="w-10 no-print"></th>
                  </tr>
                </thead>
                <tbody>
                  {chunk.map((f, i) => (
                    <tr key={f.id} className="align-top">
                      <td><InlineTextarea rows={1} value={f.designation} onChange={(v:string)=>updateRow(setEligibleFaculties, f.id, 'designation', v)} /></td>
                      <td><InlineTextarea rows={1} value={f.num} onChange={(v:string)=>updateRow(setEligibleFaculties, f.id, 'num', v)} /></td>
                      <td className="relative group">
                        <InlineTextarea rows={1} value={f.name} onChange={(v:string)=>updateRow(setEligibleFaculties, f.id, 'name', v)} />
                        <button 
                          className="no-print absolute top-1 right-1 p-1 bg-white border border-slate-200 rounded text-slate-400 hover:text-emerald-600 opacity-0 group-hover:opacity-100 transition-opacity shadow-sm"
                          onClick={() => {
                            setRowSelectedDoctorIds(new Set());
                            setRowDoctorModalId(f.id);
                          }}
                          title="Select Doctors from Faculty Table"
                        >
                          <ListPlus className="w-4 h-4" />
                        </button>
                      </td>
                      <td className="no-print text-center">
                        <button
                          className="text-red-500 hover:text-red-700 p-1 flex items-center justify-center w-full h-full"
                          onClick={() => removeRow(setEligibleFaculties, f.id)}
                          title="Delete Row"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {ci === extraEligiblePages - 1 && (
                <div className="no-print flex gap-3 mt-2 ml-8 mb-8 items-center">
                  <button
                    className="text-indigo-600 hover:text-indigo-800 text-sm flex items-center"
                    onClick={() => setEligibleFaculties(prev => [...prev, { id: generateId(), designation: '', num: '', name: '', seats: '', adequate: '' }])}
                  >
                    <Plus className="w-4 h-4 mr-1"/> Add Record
                  </button>
                </div>
              )}
              <PageFooter />
            </div>
          ))}

          {/* CONTINUATION PAGES: PG STUDYING */}
          {pgStudyingChunks.slice(1).map((chunk, ci) => (
            <div key={`pg-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={pn(9) + extraEligiblePages + ci + 1} />
              <p className="font-bold mb-2 flex pl-8 mt-4">
                <span className="w-8">iii.</span>
                <span>P.G students presently studying in the Department: (Continued)</span>
              </p>
              <table className="nmc-table tight-table text-[10pt] ml-8 w-[92%] mb-6">
                <thead>
                  <tr><th className="w-48">Name</th><th className="w-32">Joining date</th><th className="w-32">Phone No</th><th>E-mail</th><th className="w-10 no-print"></th></tr>
                </thead>
                <tbody>
                  {chunk.map(s => (
                    <tr key={s.id}>
                      <td><InlineInput value={s.name} onChange={(v:string)=>updateRow(setPgStudents, s.id, 'name', v)} /></td>
                      <td><InlineInput value={s.joiningDate} onChange={(v:string)=>updateRow(setPgStudents, s.id, 'joiningDate', v)} /></td>
                      <td><InlineInput value={s.phone} onChange={(v:string)=>updateRow(setPgStudents, s.id, 'phone', v)} /></td>
                      <td><InlineInput value={s.email} onChange={(v:string)=>updateRow(setPgStudents, s.id, 'email', v)} /></td>
                      <td className="no-print text-center">
                        <button 
                          className="text-red-500 hover:text-red-700 p-1 flex items-center justify-center w-full h-full"
                          onClick={() => removeRow(setPgStudents, s.id)}
                          title="Delete Row"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {ci === extraPgStudyingPages - 1 && (
                <div className="flex items-center gap-4 mb-6 ml-8 mt-2">
                  <button className="no-print text-indigo-600 text-sm flex items-center" onClick={()=>addRow(setPgStudents, ()=>({id:generateId(), name:'', joiningDate:'', phone:'', email:''}))}>
                    <Plus className="w-4 h-4 mr-1"/> Add Record
                  </button>
                  <button className="no-print text-emerald-600 text-sm flex items-center border border-emerald-300 rounded px-2 py-0.5" onClick={() => { setDoctorSearch(''); setSelectedDoctorIds(new Set()); setImportTarget('pgStudying'); }}>
                    <Users className="w-4 h-4 mr-1"/> Import from Doctors
                  </button>
                </div>
              )}
              <PageFooter />
            </div>
          ))}

          {/* CONTINUATION PAGES: PAST PG */}
          {pastPgChunks.slice(1).map((chunk, ci) => (
            <div key={`past-pg-cont-${ci}`} className="a4-page portrait-page print-page">
              <PageHeader pageNum={pn(9) + extraEligiblePages + extraPgStudyingPages + ci + 1} />
              <p className="font-bold mb-2 flex pl-8 mt-4">
                <span className="w-8">iv.</span>
                <span>PG students who completed their course in the last year: (Continued)</span>
              </p>
              <table className="nmc-table tight-table text-[10pt] ml-8 w-[92%] mb-6">
                <thead>
                  <tr><th className="w-48">Name</th><th className="w-24">Joining<br/>date</th><th className="w-24">Relieving<br/>Date</th><th className="w-28">Phone no</th><th>E-mail</th><th className="w-10 no-print"></th></tr>
                </thead>
                <tbody>
                  {chunk.map(s => (
                    <tr key={s.id}>
                      <td><InlineInput value={s.name} onChange={(v:string)=>updateRow(setPastPgStudents, s.id, 'name', v)} /></td>
                      <td><InlineInput value={s.joiningDate} onChange={(v:string)=>updateRow(setPastPgStudents, s.id, 'joiningDate', v)} /></td>
                      <td><InlineInput value={s.relievingDate} onChange={(v:string)=>updateRow(setPastPgStudents, s.id, 'relievingDate', v)} /></td>
                      <td><InlineInput value={s.phone} onChange={(v:string)=>updateRow(setPastPgStudents, s.id, 'phone', v)} /></td>
                      <td><InlineInput value={s.email} onChange={(v:string)=>updateRow(setPastPgStudents, s.id, 'email', v)} /></td>
                      <td className="no-print text-center">
                        <button 
                          className="text-red-500 hover:text-red-700 p-1 flex items-center justify-center w-full h-full"
                          onClick={() => removeRow(setPastPgStudents, s.id)}
                          title="Delete Row"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {ci === extraPastPgPages - 1 && (
                <div className="flex items-center gap-4 mb-8 ml-8 mt-2">
                  <button className="no-print text-indigo-600 text-sm flex items-center" onClick={()=>addRow(setPastPgStudents, ()=>({id:generateId(), name:'', joiningDate:'', relievingDate:'', phone:'', email:''}))}>
                    <Plus className="w-4 h-4 mr-1"/> Add Record
                  </button>
                  <button className="no-print text-emerald-600 text-sm flex items-center border border-emerald-300 rounded px-2 py-0.5" onClick={() => { setDoctorSearch(''); setSelectedDoctorIds(new Set()); setImportTarget('pgCompleted'); }}>
                    <Users className="w-4 h-4 mr-1"/> Import from Doctors
                  </button>
                </div>
              )}
              <PageFooter />
            </div>
          ))}
"""

    block_mod = block_mod + continuation_jsx

    new_content = content[:page9_idx] + block_mod + content[page11_idx:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Done replacing.")

if __name__ == '__main__':
    main()
