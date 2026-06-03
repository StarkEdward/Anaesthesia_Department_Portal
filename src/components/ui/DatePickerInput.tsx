import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

interface Props {
  value: string | undefined | null;
  onChange: (date: string) => void;
  className?: string;
  placeholder?: string;
  minDate?: string;
  maxDate?: string;
  required?: boolean;
}

export default function DatePickerInput({ value, onChange, className, placeholder, minDate, maxDate, required }: Props) {
  const selectedDate = React.useMemo(() => value ? new Date(value) : null, [value]);
  const min = React.useMemo(() => minDate ? new Date(minDate) : undefined, [minDate]);
  const max = React.useMemo(() => maxDate ? new Date(maxDate) : undefined, [maxDate]);

  return (
    <div className="w-full relative custom-datepicker-container">
      <DatePicker
        selected={selectedDate}
        onChange={(date: Date | null) => {
          if (date) {
            const yyyy = date.getFullYear();
            const mm = String(date.getMonth() + 1).padStart(2, '0');
            const dd = String(date.getDate()).padStart(2, '0');
            onChange(`${yyyy}-${mm}-${dd}`);
          } else {
            onChange('');
          }
        }}
        dateFormat="dd/MM/yyyy"
        showMonthDropdown
        showYearDropdown
        dropdownMode="select"
        className={className}
        placeholderText={placeholder || "dd/MM/yyyy"}
        minDate={min}
        maxDate={max}
        required={required}
        wrapperClassName="w-full"
      />
      <style>{`
        .custom-datepicker-container .react-datepicker-wrapper {
          width: 100%;
          display: block;
        }
        .custom-datepicker-container .react-datepicker__month-dropdown-container,
        .custom-datepicker-container .react-datepicker__year-dropdown-container {
          background-color: white;
          color: black;
          padding: 2px 4px;
          border-radius: 4px;
          border: 1px solid #e2e8f0;
          font-weight: 500;
        }
        .custom-datepicker-container .react-datepicker__header {
          background-color: #f8fafc;
          border-bottom: 1px solid #e2e8f0;
        }
      `}</style>
    </div>
  );
}
