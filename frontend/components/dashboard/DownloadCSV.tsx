"use client"

import React, { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button';
import { DateRange } from 'react-day-picker';

type Props = {
  date: DateRange | undefined;
}

export default function DownloadCSV({date}: Props) {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const a = date?.from?.toJSON();
      const b = date?.to?.toJSON();
      const response = await fetch(`/api/listings?before=${b}&after=${a}`);
      if (!response.ok) {
        console.error('Failed to fetch data');
        return;
      }

      const result = await response.json();
      setData(result.data);
    };

    fetchData();
  }, [date]);

  const convertToCSV = (data: any[]) => {
    const headersSet = new Set(data.flatMap(row => Object.keys(row)));
    const headers = Array.from(headersSet);
  
    const headerRow = headers.join(',');
  
    const rows = data.map(row => {
      return headers.map(header => {
        const cellValue = row[header];
        const formattedCellValue = cellValue !== undefined ? cellValue.toString().replace(/"/g, '""') : '';
        return `"${formattedCellValue}"`;
      }).join(',');
    });
  
    return [headerRow].concat(rows).join('\n');
  };

  const DownloadButton = ({ data }: { data: any[] }) => {
    const handleDownload = () => {
      if (!data || data.length === 0) {
        alert('No data available to download');
        return;
      }
  
      const csvData = convertToCSV(data);
      const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
  
      const link = document.createElement('a');
      link.href = url;
      link.download = 'data.csv';
      link.click();
  
      URL.revokeObjectURL(url);
    };

    return <Button onClick={handleDownload} disabled={!data || data.length === 0 ? true : false}>Download CSV</Button>;
  }  

  

  return (
    <DownloadButton data={data}></DownloadButton>
    // <div></div>
  )
}