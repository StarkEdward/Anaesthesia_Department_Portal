import React, { useState, useEffect, useRef } from 'react';
import { Printer, Download, Save, ArrowLeft, Loader2 } from 'lucide-react';
import { db } from '../firebase';
import { doc, getDoc, setDoc, serverTimestamp } from 'firebase/firestore';
import { useParams, useNavigate } from 'react-router-dom';
import { useToast } from '../context/ToastContext';

const generateId = () => Math.random().toString(36).substr(2, 9);

const isCenteredValue = (val: any) => {
  if (val === undefined || val === null) return false;
  const strVal = String(val);
  const trimmed = strVal.trim();
  if (trimmed === '--') return true;
  if (trimmed && !isNaN(Number(trimmed))) return true;
  return false;
};

const InlineSelect = ({ value, onChange, options, className = '' }: any) => (
  <select value={value} onChange={e => onChange(e.target.value)} className={`w-full bg-transparent border-0 border-b border-transparent hover:border-slate-300 focus:border-indigo-500 focus:ring-0 px-1 py-0.5 font-normal transition-colors appearance-none cursor-pointer `}>
    <option value=""></option>
    {options.map((opt: string) => <option key={opt} value={opt}>{opt}</option>)}
  </select>
);

const updateRow = (setter: any, id: string, field: string, value: string) => {
  setter((prev: any[]) => prev.map(item => item.id === id ? { ...item, [field]: value } : item));
};

const InlineInput = ({ value, onChange, placeholder = '', className = '', onBlur, list }: any) => (
  <input type="text" value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} onBlur={onBlur} list={list}
    className={`w-full bg-transparent border-0 border-b border-transparent hover:border-slate-300 focus:border-indigo-500 focus:ring-0 px-1 py-0.5 font-normal transition-colors ${isCenteredValue(value) ? 'text-center' : ''} ${className}`} />
);

export default function NMCFormA() {
  const { showToast } = useToast();
  const printRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);
  const { id } = useParams();
  const navigate = useNavigate();

  // Basic Info State
  const [instInfo, setInstInfo] = useState({
    name: '',
    type: '',
    standalone: '',
    periodFrom: '',
    periodTo: '',
    date: ''
  });

  const [genInfo, setGenInfo] = useState({
    name: '',
    type: '',
    standalone: '',
    lopDate: '',
    workingDays: '',
    address: '',
    city: '',
    district: '',
    state: '',
    pinCode: '',
    website: '',
    email: '',
    landline: '',
    mobile: '',
    competentAuthorityName: '',
    competentAuthorityEmail: '',
    competentAuthorityMobile: '',
    competentAuthorityLandline: '',
    affiliatedUniversity: '',
    viceChancellorName: '',
    viceChancellorPhone: '',
    viceChancellorEmail: ''
  });

  const [ugDetail, setUgDetail] = useState({
    seats: '',
    beds: '',
    opdDay: '', opdYr1: '', opdYr2: '', opdYr3: '',
    bedOccDay: '', bedOccYr1: '', bedOccYr2: '', bedOccYr3: ''
  });

  const [departments, setDepartments] = useState([
    { id: generateId(), name: '', beds: '', units: '', admissions: '', startYear: '' },
    { id: generateId(), name: '', beds: '', units: '', admissions: '', startYear: '' },
    { id: generateId(), name: '', beds: '', units: '', admissions: '', startYear: '' },
    { id: generateId(), name: '', beds: '', units: '', admissions: '', startYear: '' },
    { id: generateId(), name: '', beds: '', units: '', admissions: '', startYear: '' }
  ]);

  const [commonInfra, setCommonInfra] = useState({
    oxygenAvail: '', oxygenAdeq: '',
    suctionAvail: '', suctionAdeq: '',
    sterilizationAvail: '', sterilizationAdeq: '',
    laundryAvail: '', laundryAdeq: '',
    kitchenAvail: '', kitchenAdeq: '',
    generatorAvail: '', generatorAdeq: '',
    bioWasteAvail: '', bioWasteAdeq: '',
    medRecordAvail: '', medRecordAdeq: '',
    icdAvail: '', icdAdeq: ''
  });

  const [opd, setOpd] = useState({
    space: '',
    patientsDay: '', patientsYr1: '', patientsYr2: '', patientsYr3: ''
  });

  const [bloodBank, setBloodBank] = useState({
    licenseDate: '',
    componentFacility: '',
    issuedDay: '', issuedYr1: '', issuedYr2: '', issuedYr3: '',
    utilizedDay: '', utilizedYr1: '', utilizedYr2: '', utilizedYr3: '',
    dailyDay: '', dailyYr1: '', dailyYr2: '', dailyYr3: '',
    collectedDay: '', collectedYr1: '', collectedYr2: '', collectedYr3: '',
    crossMatchDay: '', crossMatchYr1: '', crossMatchYr2: '', crossMatchYr3: ''
  });

  useEffect(() => {
    if (id && id !== 'new') {
      const fetchData = async () => {
        setLoading(true);
        try {
          const docRef = doc(db, 'nmc_form_a', id);
          const docSnap = await getDoc(docRef);
          if (docSnap.exists()) {
            const data = docSnap.data();
            setInstInfo(data.instInfo || {});
            setGenInfo(data.genInfo || {});
            if (data.ugDetail) setUgDetail(data.ugDetail);
            if (data.departments && data.departments.length > 0) setDepartments(data.departments);
            if (data.commonInfra) setCommonInfra(data.commonInfra);
            if (data.opd) setOpd(data.opd);
            if (data.bloodBank) setBloodBank(data.bloodBank);
          } else {
            showToast("Record not found", "error");
            navigate('/nmc-form-a');
          }
        } catch (error) {
          console.error("Error fetching data:", error);
          showToast("Error loading record", "error");
        } finally {
          setLoading(false);
        }
      };
      fetchData();
    }
  }, [id, navigate, showToast]);

  const handleSave = async () => {
    setLoading(true);
    try {
      const recordId = id && id !== 'new' ? id : generateId();
      const payload = {
        instInfo,
        genInfo,
        ugDetail,
        departments,
        commonInfra,
        opd,
        bloodBank,
        updatedAt: serverTimestamp(),
      };
      await setDoc(doc(db, 'nmc_form_a', recordId), payload, { merge: true });
      showToast("Form saved successfully!", "success");
      if (!id || id === 'new') {
        navigate(`/nmc-form-a/${recordId}`, { replace: true });
      }
    } catch (error) {
      console.error("Error saving form:", error);
      showToast("Error saving form", "error");
    } finally {
      setLoading(false);
    }
  };

  const handlePrintClick = () => window.print();

  const PageHeader = ({ pageNum }: { pageNum: number }) => (
    <div className="flex justify-between w-full mb-3 font-serif text-[11pt]">
      <div>STANDARD ASSESSMENT FORM-A/2024</div>
      <div>{pageNum}</div>
    </div>
  );

  const PageFooter = () => (
    <div className="absolute bottom-[12.7mm] left-[12.7mm] right-[12.7mm] flex justify-between text-[11pt] font-serif font-bold">
      <div>Signature of Dean</div>
      <div>Signature of Assessor</div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-serif print:bg-white print:min-h-0">
      {/* ACTION BAR */}
      <div className="no-print sticky top-0 z-40 bg-white border-b border-slate-200 shadow-sm px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/nmc-form-a')} className="text-slate-500 hover:text-slate-700 flex items-center gap-1 text-sm font-sans font-medium transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to List
          </button>
          <div className="h-6 w-px bg-slate-200"></div>
          <h1 className="text-lg font-bold text-slate-800 font-sans">
            NMC Form A {id && id !== 'new' ? <span className="text-slate-400 font-normal text-sm ml-2">ID: {id.substring(0,8)}</span> : <span className="text-emerald-500 font-normal text-sm ml-2">New Draft</span>}
          </h1>
        </div>
        <div className="flex items-center gap-3 font-sans">
          <button onClick={handleSave} disabled={loading} className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors shadow-sm text-sm font-medium disabled:opacity-50">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            Save Draft
          </button>
          <button onClick={handlePrintClick} className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-sm text-sm font-medium">
            <Printer className="w-4 h-4" /> Print / Save PDF
          </button>
        </div>
      </div>

      {/* FORM PAGES CONTAINER */}
      <div className="flex-1 overflow-auto py-8 print:py-0 print:overflow-visible flex flex-col items-center gap-8 print:gap-0" ref={printRef}>
        
        {/* PAGE 1 */}
        <div className="a4-page portrait-page print-page relative">
          <PageHeader pageNum={1} />
          
          <div className="flex items-center justify-center mb-6 relative">
            <div className="absolute left-0">
              <img src="/nmc-logo.png" alt="NMC Logo" className="h-24 object-contain" />
            </div>
            <div className="text-center flex-1">
              <h2 className="text-[14pt] font-bold mb-2">POST-GRADUATE MEDICAL EDUCATION BOARD</h2>
              <h3 className="text-[14pt] font-bold">NATIONAL MEDICAL COMMISSION</h3>
            </div>
          </div>

          <div className="text-center mb-6">
            <h1 className="text-[16pt] font-bold underline underline-offset-4 mb-2">STANDARD ASSESSMENT FORM-A</h1>
            <p className="text-[12pt]">(Institutional Information Common for <span className="font-bold">all PG Specialities</span>)</p>
          </div>

          <div className="text-center mb-6">
            <h2 className="text-[14pt] font-bold underline underline-offset-4">INSTITUTIONAL INFORMATION</h2>
          </div>

          <div className="space-y-4 text-[12pt] mb-6">
            <div className="flex items-center">
              <span className="w-48 whitespace-nowrap">Name of Institution:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={instInfo.name} onChange={(v:string) => setInstInfo({...instInfo, name: v})} /></span>
            </div>
            <div className="flex items-center">
              <span className="w-64 whitespace-nowrap">Government/ Non-Government:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={instInfo.type} onChange={(v:string) => setInstInfo({...instInfo, type: v})} /></span>
            </div>
            <div className="flex items-center gap-4">
              <span className="whitespace-nowrap">Standalone PG:</span>
              <span className="font-bold">Yes/ No</span>
              <span className="flex-1 border-b border-black"><InlineInput value={instInfo.standalone} onChange={(v:string) => setInstInfo({...instInfo, standalone: v})} /></span>
            </div>
            <div className="flex items-center gap-2">
              <span className="whitespace-nowrap">Period:</span>
              <span className="w-48 border-b border-black"><InlineInput value={instInfo.periodFrom} onChange={(v:string) => setInstInfo({...instInfo, periodFrom: v})} /></span>
              <span className="whitespace-nowrap">to</span>
              <span className="w-48 border-b border-black"><InlineInput value={instInfo.periodTo} onChange={(v:string) => setInstInfo({...instInfo, periodTo: v})} /></span>
            </div>
            <div className="flex items-center">
              <span className="w-40 whitespace-nowrap">Date of the Report:</span>
              <span className="w-64 border-b border-black"><InlineInput value={instInfo.date} onChange={(v:string) => setInstInfo({...instInfo, date: v})} /></span>
            </div>
          </div>

          <div className="border-b-2 border-black mb-1 w-full"></div>
          <div className="text-center font-bold italic text-[11pt] mb-2">
            INSTRUCTIONS TO DEAN/ DIRECTOR/PRINCIPAL & HEAD OF THE DEPARTMENT
          </div>

          <ol className="list-decimal pl-6 space-y-3 text-[11.5pt] text-justify leading-snug">
            <li>
              This Standard Assessment Form is meant for the purpose of giving Annual Disclosure Report (<span className="font-bold">Annual Self-Declaration</span>) by Medical Colleges/Institutions as required under <span className="font-bold">Section 4</span> of MSMER-2023 regulation and for the Assessment/Inspection of a medical college/an institution by the Assessor. It will be in <span className="font-bold">Three Parts:</span>
              <ol className="list-[lower-roman] pl-10 mt-2 space-y-1">
                <li><span className="font-bold">Form-A</span> is for the Institutional Information and is common for all PG Specialities.</li>
                <li><span className="font-bold">Form-B</span> is for Speciality specific information (<span className="font-bold">Broad/Super Speciality</span>).</li>
                <li>Faculty, Senior Resident and Post-Graduate Students Declaration Forms.</li>
              </ol>
            </li>
            <li>These Forms will be updated/modified from time to time. Please download it afresh at the time of any application/submission.</li>
            <li>For the purpose of Annual Disclosure Report (<span className="font-bold">Annual Self-Declaration</span>), the Data of previous year (1<sup>st</sup> January to 31<sup>st</sup> December) will be considered.</li>
            <li>Medical college/institution will fill up all the details/data. The Assessor will verify availability and functional status of major infrastructure and major equipment of the institution mentioned in <span className="font-bold">Form-A</span> and may verify the relevant workload data furnished by the medical college/institution as per the requirement. Assessor will verify in detail all the items mentioned in <span className="font-bold">Form-B</span> (Department Specific form).</li>
            <li>The original copy of the Annual Self-Declaration Form shall be preserved by the medical colleges. The PDF copy of SAF will be sent by e-mail.</li>
            <li>Please read the FORM carefully before filling it up. Retrospective changes in Data will not be allowed.</li>
            <li>Do NOT edit or modify any part of the Form. Tampering with the format of this Form will render your submission invalid.</li>
            <li>Write <span className="font-bold">N/A</span> where it is <span className="font-bold">not applicable</span>. Write <span className="font-bold">'Not Available'</span>, if the facility is <span className="font-bold">not available</span>.</li>
            <li>Head of the Department and Dean will be responsible for filling all columns and signing on all pages and at the end of the Form. Do NOT leave any section of the Form or part thereof unanswered. Incompletely filled up Form shall be summarily rejected.</li>
          </ol>

          <PageFooter />
        </div>

        {/* PAGE 2 */}
        <div className="a4-page portrait-page print-page relative">
          <PageHeader pageNum={2} />
          
          <ol start={10} className="list-decimal pl-6 space-y-3 text-[11.5pt] text-justify leading-snug">
            <li>Dean, Head of Department (HoD) and Faculty should be thoroughly well-versed with all Regulations and MSRs of NMC.</li>
            <li>All Faculty, Senior Residents and Post-Graduate students will fill up the <span className="font-bold">respective Declaration Forms</span>. It should be countersigned by HoD and Head of the institution. The original Declaration Form shall be preserved by the medical colleges/institutions.</li>
            <li>Medical College shall maintain the <span className="font-bold">Declaration Forms</span> who are relieved or retired during the reported year.</li>
            <li>Add rows in a Table as per requirement.</li>
            <li>Non-compliance/wrong declaration or fake documents will invite penalties as per NMC regulations.</li>
            <li>The working days will be calculated as per the following formula [365 - 52 (Sundays) -Holidays declared by the respective Government/medical college]. The dates of the Holidays to be provided by the medical college/institution as Annexure.</li>
            <li>Annual detail of all clinical workload/ investigations will be provided as per the <span className="font-bold">Data Table</span> as and when asked for. Template of the Data Table is at end of this document.</li>
          </ol>

          <PageFooter />
        </div>

        {/* PAGE 3 */}
        <div className="a4-page portrait-page print-page relative">
          <PageHeader pageNum={3} />
          
          <div className="flex mb-6 text-[12pt] font-bold">
            <span className="w-12">A.</span>
            <span className="underline underline-offset-4 w-full text-center block -ml-12">GENERAL INFORMATION OF MEDICAL COLLEGE/ INSTITUTION</span>
          </div>

          <div className="space-y-4 text-[11.5pt] pl-4">
            <div className="flex items-center">
              <span className="w-8">1.</span>
              <span className="w-80">Name of Medical College/Institution:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.name} onChange={(v:string)=>setGenInfo({...genInfo, name: v})} /></span>
            </div>
            
            <div className="flex items-center">
              <span className="w-8">2.</span>
              <span className="w-80">College Type: Government/ Non-Government:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.type} onChange={(v:string)=>setGenInfo({...genInfo, type: v})} /></span>
            </div>

            <div className="flex items-center gap-4">
              <span className="w-8">3.</span>
              <span className="w-40">Stand-alone PG:</span>
              <span className="font-bold w-20">Yes/No</span>
              <span className="w-32 border-b border-black"><InlineInput value={genInfo.standalone} onChange={(v:string)=>setGenInfo({...genInfo, standalone: v})} /></span>
            </div>

            <div className="flex items-center">
              <span className="w-8">4.</span>
              <span className="w-[450px]">LOP date of establishment of undergraduate college:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.lopDate} onChange={(v:string)=>setGenInfo({...genInfo, lopDate: v})} /></span>
            </div>

            <div className="flex items-center gap-6">
              <span className="w-8">5.</span>
              <span>Dates of the Holidays of last year.</span>
              <span className="font-bold">Attach file as Annexure.</span>
            </div>

            <div className="flex items-center">
              <span className="w-8">6.</span>
              <span className="w-64">Total working days of last year:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.workingDays} onChange={(v:string)=>setGenInfo({...genInfo, workingDays: v})} /></span>
            </div>

            <div className="flex items-center mt-6">
              <span className="w-8">7.</span>
              <span className="w-64">College Address:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.address} onChange={(v:string)=>setGenInfo({...genInfo, address: v})} /></span>
            </div>
            <div className="flex items-center pl-8">
              <span className="w-64">College City/Town:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.city} onChange={(v:string)=>setGenInfo({...genInfo, city: v})} /></span>
            </div>
            <div className="flex items-center pl-8">
              <span className="w-64">College District:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.district} onChange={(v:string)=>setGenInfo({...genInfo, district: v})} /></span>
            </div>
            <div className="flex items-center pl-8">
              <span className="w-64">College State:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.state} onChange={(v:string)=>setGenInfo({...genInfo, state: v})} /></span>
            </div>
            <div className="flex items-center pl-8">
              <span className="w-64">Pin Code:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.pinCode} onChange={(v:string)=>setGenInfo({...genInfo, pinCode: v})} /></span>
            </div>

            <div className="flex items-center mt-6">
              <span className="w-8">8.</span>
              <span className="w-64">College Website:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.website} onChange={(v:string)=>setGenInfo({...genInfo, website: v})} /></span>
            </div>
            
            <div className="flex items-center">
              <span className="w-8">9.</span>
              <span className="w-64">College E-mail ID:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.email} onChange={(v:string)=>setGenInfo({...genInfo, email: v})} /></span>
            </div>
            
            <div className="flex items-center">
              <span className="w-8">10.</span>
              <span className="w-64">College Landline No.:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.landline} onChange={(v:string)=>setGenInfo({...genInfo, landline: v})} /></span>
            </div>
            
            <div className="flex items-center">
              <span className="w-8">11.</span>
              <span className="w-64">College Mobile/Phone No.:</span>
              <span className="w-96 border-b border-black"><InlineInput value={genInfo.mobile} onChange={(v:string)=>setGenInfo({...genInfo, mobile: v})} /></span>
            </div>

            <div className="flex items-center mt-6 mb-4">
              <span className="w-8">12.</span>
              <span className="w-72">College Competent Authority:</span>
              <span className="font-bold text-[12pt]">Dean/ Director/ Principal</span>
            </div>

            <div className="flex items-center">
              <span className="w-8">13.</span>
              <span className="w-[300px]">College Competent Authority Name:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.competentAuthorityName} onChange={(v:string)=>setGenInfo({...genInfo, competentAuthorityName: v})} /></span>
            </div>

            <div className="flex items-center">
              <span className="w-8">14.</span>
              <span className="w-[300px]">College Competent Authority E-mail ID:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.competentAuthorityEmail} onChange={(v:string)=>setGenInfo({...genInfo, competentAuthorityEmail: v})} /></span>
            </div>

            <div className="flex items-center">
              <span className="w-8">15.</span>
              <span className="w-[300px]">College Competent Authority Mobile No:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.competentAuthorityMobile} onChange={(v:string)=>setGenInfo({...genInfo, competentAuthorityMobile: v})} /></span>
            </div>

            <div className="flex items-center">
              <span className="w-8">16.</span>
              <span className="w-[300px]">College Competent Authority Landline No:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.competentAuthorityLandline} onChange={(v:string)=>setGenInfo({...genInfo, competentAuthorityLandline: v})} /></span>
            </div>

            <div className="flex items-center mt-6">
              <span className="w-8">17.</span>
              <span className="w-[300px]">Name and Address of Affiliated University:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.affiliatedUniversity} onChange={(v:string)=>setGenInfo({...genInfo, affiliatedUniversity: v})} /></span>
            </div>

            <div className="flex items-center">
              <span className="w-8">18.</span>
              <span className="w-[300px]">Name and address of the Vice-Chancellor:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.viceChancellorName} onChange={(v:string)=>setGenInfo({...genInfo, viceChancellorName: v})} /></span>
            </div>

            <div className="flex items-center">
              <span className="w-8">19.</span>
              <span className="w-[300px]">Landline No./Mobile No of the Vice-Chancellor:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.viceChancellorPhone} onChange={(v:string)=>setGenInfo({...genInfo, viceChancellorPhone: v})} /></span>
            </div>

            <div className="flex items-center">
              <span className="w-8">20.</span>
              <span className="w-[300px]">E-mail address of the Vice-Chancellor:</span>
              <span className="flex-1 border-b border-black"><InlineInput value={genInfo.viceChancellorEmail} onChange={(v:string)=>setGenInfo({...genInfo, viceChancellorEmail: v})} /></span>
            </div>

          </div>

          <PageFooter />
        </div>
        {/* PAGE 4 */}
        <div className="a4-page portrait-page print-page relative">
          <PageHeader pageNum={4} />

          <div className="flex mb-4 text-[11.5pt] font-bold">
            <span className="w-12">B.</span>
            <span className="underline w-full">DETAIL OF UNDERGRADUATE MEDICAL COLLEGE/INSTITUTE:</span>
          </div>

          <div className="pl-12 space-y-3 text-[11.5pt] mb-6">
            <div className="flex items-center">
              <span className="w-[350px]">Total number of UG seats:</span>
              <span className="w-48 border-b border-black"><InlineInput value={ugDetail.seats} onChange={(v:string)=>setUgDetail({...ugDetail, seats: v})} /></span>
            </div>
            <div className="flex items-center">
              <span className="w-[450px]">Total hospital beds of all Departments required for UG College:</span>
              <span className="w-48 border-b border-black"><InlineInput value={ugDetail.beds} onChange={(v:string)=>setUgDetail({...ugDetail, beds: v})} /></span>
            </div>
          </div>

          <table className="nmc-table text-[11pt] w-full mb-8">
            <thead>
              <tr>
                <th className="w-[30%]">Parameter</th>
                <th className="w-[18%]">On the day of<br/>Assessment</th>
                <th className="w-[15%]">Year 1</th>
                <th className="w-[15%]">Year 2</th>
                <th className="w-[22%]">Year 3<br/>(Last Year)</th>
              </tr>
              <tr className="text-center font-bold">
                <td>(1)</td><td>(2)</td><td>(3)</td><td>(4)</td><td>(5)</td>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="pl-2 pr-2 text-justify">
                  Total OPD patients of all departments required for UG college
                  <br/><span className="italic text-[10pt] font-normal">(Write the average of all the OPD days in a year in column 3, 4, 5)</span>
                </td>
                <td><InlineInput value={ugDetail.opdDay} onChange={(v:string)=>setUgDetail({...ugDetail, opdDay: v})} /></td>
                <td><InlineInput value={ugDetail.opdYr1} onChange={(v:string)=>setUgDetail({...ugDetail, opdYr1: v})} /></td>
                <td><InlineInput value={ugDetail.opdYr2} onChange={(v:string)=>setUgDetail({...ugDetail, opdYr2: v})} /></td>
                <td><InlineInput value={ugDetail.opdYr3} onChange={(v:string)=>setUgDetail({...ugDetail, opdYr3: v})} /></td>
              </tr>
              <tr>
                <td className="pl-2 pr-2 text-justify">
                  Bed Occupancy of all the required In-patient beds for UG College.
                  <br/><span className="italic text-[10pt] font-normal">(Write average of all days in a year in column 3, 4, 5)</span>
                </td>
                <td><InlineInput value={ugDetail.bedOccDay} onChange={(v:string)=>setUgDetail({...ugDetail, bedOccDay: v})} /></td>
                <td><InlineInput value={ugDetail.bedOccYr1} onChange={(v:string)=>setUgDetail({...ugDetail, bedOccYr1: v})} /></td>
                <td><InlineInput value={ugDetail.bedOccYr2} onChange={(v:string)=>setUgDetail({...ugDetail, bedOccYr2: v})} /></td>
                <td><InlineInput value={ugDetail.bedOccYr3} onChange={(v:string)=>setUgDetail({...ugDetail, bedOccYr3: v})} /></td>
              </tr>
            </tbody>
          </table>

          <div className="flex mb-4 text-[11.5pt] font-bold">
            <span className="w-12">C.</span>
            <span className="w-full">LIST OF ALL BROAD SPECIALITY AND SUPER SPECIALITY DEPARTMENTS EXISTING IN THE INSTITUTION WITH BASIC DETAILS:</span>
          </div>

          <table className="nmc-table tight-table text-[10.5pt] w-full mb-8">
            <thead>
              <tr>
                <th className="w-[35%]">Name of Department</th>
                <th className="w-[15%]">Total Beds</th>
                <th className="w-[15%]">Total No. of<br/>Units</th>
                <th className="w-[18%]">Total No. of<br/>Admissions<br/>per year</th>
                <th className="w-[17%]">Year of<br/>Starting the<br/>Course</th>
              </tr>
            </thead>
            <tbody>
              {departments.map((dep, idx) => (
                <tr key={dep.id}>
                  <td><InlineInput value={dep.name} onChange={(v:string)=>updateRow(setDepartments, dep.id, 'name', v)} /></td>
                  <td><InlineInput value={dep.beds} onChange={(v:string)=>updateRow(setDepartments, dep.id, 'beds', v)} /></td>
                  <td><InlineInput value={dep.units} onChange={(v:string)=>updateRow(setDepartments, dep.id, 'units', v)} /></td>
                  <td><InlineInput value={dep.admissions} onChange={(v:string)=>updateRow(setDepartments, dep.id, 'admissions', v)} /></td>
                  <td><InlineInput value={dep.startYear} onChange={(v:string)=>updateRow(setDepartments, dep.id, 'startYear', v)} /></td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="flex mb-4 text-[11.5pt] font-bold">
            <span className="w-12">D.</span>
            <span className="w-full">COMMON INFRASTRUCTURE:</span>
          </div>
          
          <div className="flex mb-2 text-[11.5pt] font-bold pl-8">
            <span className="w-8">I.</span>
            <span className="w-full">General:</span>
          </div>

          <table className="nmc-table text-[11pt] w-[80%] mx-auto">
            <thead>
              <tr>
                <th className="w-[45%]">Parameters</th>
                <th className="w-[25%]">Availability</th>
                <th className="w-[30%]">Adequate/ Not<br/>Adequate</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="pl-2">Central supply of Oxygen</td>
                <td className="text-center font-bold"><InlineSelect value={commonInfra.oxygenAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, oxygenAvail: v})} options={['Yes', 'No']} /></td>
                <td><InlineSelect value={commonInfra.oxygenAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, oxygenAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
            </tbody>
          </table>

          <PageFooter />
        </div>

        {/* PAGE 5 */}
        <div className="a4-page portrait-page print-page relative">
          <PageHeader pageNum={5} />

          <table className="nmc-table text-[11pt] w-[80%] mx-auto mb-8 border-t-0 -mt-8">
            <tbody>
              <tr>
                <td className="w-[45%] pl-2 border-t-0">Central Suction</td>
                <td className="w-[25%] text-center font-bold border-t-0"><InlineSelect value={commonInfra.suctionAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, suctionAvail: v})} options={['Yes', 'No']} /></td>
                <td className="w-[30%] border-t-0"><InlineSelect value={commonInfra.suctionAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, suctionAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
              <tr>
                <td className="pl-2">Central Sterilization Department</td>
                <td className="text-center font-bold"><InlineSelect value={commonInfra.sterilizationAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, sterilizationAvail: v})} options={['Yes', 'No']} /></td>
                <td><InlineSelect value={commonInfra.sterilizationAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, sterilizationAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
              <tr>
                <td className="pl-2">Laundry</td>
                <td className="text-center font-bold"><InlineSelect value={commonInfra.laundryAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, laundryAvail: v})} options={['Yes', 'No']} /></td>
                <td><InlineSelect value={commonInfra.laundryAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, laundryAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
              <tr>
                <td className="pl-2">Kitchen</td>
                <td className="text-center font-bold"><InlineSelect value={commonInfra.kitchenAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, kitchenAvail: v})} options={['Yes', 'No']} /></td>
                <td><InlineSelect value={commonInfra.kitchenAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, kitchenAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
              <tr>
                <td className="pl-2">Generator facility</td>
                <td className="text-center font-bold"><InlineSelect value={commonInfra.generatorAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, generatorAvail: v})} options={['Yes', 'No']} /></td>
                <td><InlineSelect value={commonInfra.generatorAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, generatorAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
              <tr>
                <td className="pl-2">Bio-waste disposal</td>
                <td className="text-center font-bold"><InlineSelect value={commonInfra.bioWasteAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, bioWasteAvail: v})} options={['Yes', 'No']} /></td>
                <td><InlineSelect value={commonInfra.bioWasteAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, bioWasteAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
              <tr>
                <td className="pl-2">Computerized Medical Record Section</td>
                <td className="text-center font-bold"><InlineSelect value={commonInfra.medRecordAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, medRecordAvail: v})} options={['Yes', 'No']} /></td>
                <td><InlineSelect value={commonInfra.medRecordAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, medRecordAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
              <tr>
                <td className="pl-2">Which ICD classification being used</td>
                <td className="text-center font-bold"><InlineSelect value={commonInfra.icdAvail} onChange={(v:string)=>setCommonInfra({...commonInfra, icdAvail: v})} options={['ICD10', 'ICD11']} /></td>
                <td><InlineSelect value={commonInfra.icdAdeq} onChange={(v:string)=>setCommonInfra({...commonInfra, icdAdeq: v})} options={['Adequate', 'Not Adequate']} /></td>
              </tr>
            </tbody>
          </table>

          <div className="flex mb-4 text-[11.5pt] font-bold pl-8">
            <span className="w-8">II.</span>
            <span className="w-full">Out-Patient Department:</span>
          </div>

          <div className="flex items-center mb-2 text-[11pt] pl-16">
            <span className="w-64">Space and arrangements</span>
            <span className="w-8">:</span>
            <span className="w-48"><InlineSelect value={opd.space} onChange={(v:string)=>setOpd({...opd, space: v})} options={['Adequate', 'Not Adequate']} /></span>
          </div>

          <table className="nmc-table text-[11pt] w-full mb-8">
            <thead>
              <tr>
                <th className="w-[30%]">Parameter</th>
                <th className="w-[18%]">On the day of<br/>Assessment</th>
                <th className="w-[15%]">Year 1</th>
                <th className="w-[15%]">Year 2</th>
                <th className="w-[22%]">Year 3<br/>(Last Year)</th>
              </tr>
              <tr className="text-center font-bold">
                <td>(1)</td><td>(2)</td><td>(3)</td><td>(4)</td><td>(5)</td>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="pl-2 pr-2 font-bold">
                  Total OPD Patients of all the Departments in the hospital
                  <br/><span className="italic text-[10pt] font-normal">(Write the average of all the OPD days in a year in column 3, 4, 5)</span>
                </td>
                <td><InlineInput value={opd.patientsDay} onChange={(v:string)=>setOpd({...opd, patientsDay: v})} /></td>
                <td><InlineInput value={opd.patientsYr1} onChange={(v:string)=>setOpd({...opd, patientsYr1: v})} /></td>
                <td><InlineInput value={opd.patientsYr2} onChange={(v:string)=>setOpd({...opd, patientsYr2: v})} /></td>
                <td><InlineInput value={opd.patientsYr3} onChange={(v:string)=>setOpd({...opd, patientsYr3: v})} /></td>
              </tr>
            </tbody>
          </table>

          <div className="flex mb-4 text-[11.5pt] font-bold pl-8">
            <span className="w-8">III.</span>
            <span className="w-full">Blood Bank:</span>
          </div>

          <div className="pl-16 space-y-4 text-[11.5pt] mb-4">
            <div className="flex items-center">
              <span className="w-64">License valid till date:</span>
              <span className="w-64 border-b border-black"><InlineInput value={bloodBank.licenseDate} onChange={(v:string)=>setBloodBank({...bloodBank, licenseDate: v})} /></span>
            </div>
            <div className="flex items-center">
              <span className="w-64">Blood component facility:</span>
              <span className="font-bold"><InlineSelect value={bloodBank.componentFacility} onChange={(v:string)=>setBloodBank({...bloodBank, componentFacility: v})} options={['Available', 'Not Available']} /></span>
            </div>
          </div>

          <table className="nmc-table tight-table text-[10.5pt] w-full">
            <thead>
              <tr>
                <th className="w-[30%]">Parameter</th>
                <th className="w-[18%]">On the day<br/>of<br/>Assessment</th>
                <th className="w-[15%]">Year 1</th>
                <th className="w-[15%]">Year 2</th>
                <th className="w-[22%]">Year 3<br/>(Last Year)</th>
              </tr>
              <tr className="text-center font-bold">
                <td>(1)</td><td>(2)</td><td>(3)</td><td>(4)</td><td>(5)</td>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="pl-2">Blood Units including Components issued</td>
                <td><InlineInput value={bloodBank.issuedDay} onChange={(v:string)=>setBloodBank({...bloodBank, issuedDay: v})} /></td>
                <td><InlineInput value={bloodBank.issuedYr1} onChange={(v:string)=>setBloodBank({...bloodBank, issuedYr1: v})} /></td>
                <td><InlineInput value={bloodBank.issuedYr2} onChange={(v:string)=>setBloodBank({...bloodBank, issuedYr2: v})} /></td>
                <td><InlineInput value={bloodBank.issuedYr3} onChange={(v:string)=>setBloodBank({...bloodBank, issuedYr3: v})} /></td>
              </tr>
              <tr>
                <td className="pl-2">Blood Units including Components utilized in the hospital <span className="italic">(write average of all days in column 3,4,5)</span></td>
                <td><InlineInput value={bloodBank.utilizedDay} onChange={(v:string)=>setBloodBank({...bloodBank, utilizedDay: v})} /></td>
                <td><InlineInput value={bloodBank.utilizedYr1} onChange={(v:string)=>setBloodBank({...bloodBank, utilizedYr1: v})} /></td>
                <td><InlineInput value={bloodBank.utilizedYr2} onChange={(v:string)=>setBloodBank({...bloodBank, utilizedYr2: v})} /></td>
                <td><InlineInput value={bloodBank.utilizedYr3} onChange={(v:string)=>setBloodBank({...bloodBank, utilizedYr3: v})} /></td>
              </tr>
              <tr>
                <td className="pl-2">Average number of units utilized daily by the various Specialities <span className="italic font-bold">(Attach Annexure)</span></td>
                <td><InlineInput value={bloodBank.dailyDay} onChange={(v:string)=>setBloodBank({...bloodBank, dailyDay: v})} /></td>
                <td><InlineInput value={bloodBank.dailyYr1} onChange={(v:string)=>setBloodBank({...bloodBank, dailyYr1: v})} /></td>
                <td><InlineInput value={bloodBank.dailyYr2} onChange={(v:string)=>setBloodBank({...bloodBank, dailyYr2: v})} /></td>
                <td><InlineInput value={bloodBank.dailyYr3} onChange={(v:string)=>setBloodBank({...bloodBank, dailyYr3: v})} /></td>
              </tr>
              <tr>
                <td className="pl-2">Blood units collected</td>
                <td><InlineInput value={bloodBank.collectedDay} onChange={(v:string)=>setBloodBank({...bloodBank, collectedDay: v})} /></td>
                <td><InlineInput value={bloodBank.collectedYr1} onChange={(v:string)=>setBloodBank({...bloodBank, collectedYr1: v})} /></td>
                <td><InlineInput value={bloodBank.collectedYr2} onChange={(v:string)=>setBloodBank({...bloodBank, collectedYr2: v})} /></td>
                <td><InlineInput value={bloodBank.collectedYr3} onChange={(v:string)=>setBloodBank({...bloodBank, collectedYr3: v})} /></td>
              </tr>
              <tr>
                <td className="pl-2">Total Number of Cross matchings</td>
                <td><InlineInput value={bloodBank.crossMatchDay} onChange={(v:string)=>setBloodBank({...bloodBank, crossMatchDay: v})} /></td>
                <td><InlineInput value={bloodBank.crossMatchYr1} onChange={(v:string)=>setBloodBank({...bloodBank, crossMatchYr1: v})} /></td>
                <td><InlineInput value={bloodBank.crossMatchYr2} onChange={(v:string)=>setBloodBank({...bloodBank, crossMatchYr2: v})} /></td>
                <td><InlineInput value={bloodBank.crossMatchYr3} onChange={(v:string)=>setBloodBank({...bloodBank, crossMatchYr3: v})} /></td>
              </tr>
            </tbody>
          </table>

          <PageFooter />
        </div>
      </div>
    </div>
  );
}



