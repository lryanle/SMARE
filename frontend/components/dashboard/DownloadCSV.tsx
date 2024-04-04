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

  useEffect(() => {
    console.log(data)
  }, [data])

  const convertToCSV = (data: any) => {
    const headers = Object.keys(data[0]).join(',');
    const rows = data.map((row: any) => 
      Object.values(row).map((value: any) => 
        `"${value.toString().replace(/"/g, '""')}"`).join(',')
    );

    return [headers].concat(rows).join('\n');
  };

  const DownloadButton = ({ data }: { data: any[] }) => {
    const handleDownload = () => {
      console.log(data)
      if (!data || data.length === 0) {
        alert('No data available to download');
        return;
      }
  
      // Log data for debugging
      console.log('Downloading data:', data);
  
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