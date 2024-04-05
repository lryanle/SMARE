"use client";

import { useState, useEffect } from 'react';
import { DateRange } from 'react-day-picker';
import { BarChart, Bar, Brush, ReferenceLine, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area, ComposedChart, LineChart, Line } from 'recharts';

type Props = {
  date: DateRange | undefined;
};

export function Overview({ date }: Props) {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const a = date?.from?.toJSON();
      const b = date?.to?.toJSON();
      const response = await fetch(`/api/listings/day?before=${b}&after=${a}`);
      if (!response.ok) {
        console.error('Failed to fetch data');
        return;
      }

      const result = await response.json();
      if (result.success && result.data) {
        const transformedData = result.data.map((item: any) => ({
          ...item,
          formattedDate: item.name.substring(5).replace(/-/g, '/')
        }));
        setData(transformedData);
      }
    };

    fetchData();
  }, [date]);


  return (
    <ResponsiveContainer width="100%" height={384}>
      <ComposedChart
        width={500}
        height={400}
        data={data}
        margin={{
          top: 20,
          right: 60,
          bottom: 20,
          left: 20,
        }}
      >
        <CartesianGrid strokeDasharray="4 4" />
        <XAxis dataKey="formattedDate" scale="band" />
        <YAxis label={{ value: "Total", angle: -90, position: "insideLeft" }}/>
        <Tooltip />
        <Legend verticalAlign="top" wrapperStyle={{ lineHeight: '40px' }} />
        <Brush dataKey="formattedDate" height={30} stroke="#000000cc">
          <LineChart>
            <Line dataKey="total" stroke="#000000cc" dot={false} />
          </LineChart>
        </Brush>
        <Area type="monotone" name="Flagged" dataKey="flaggedTrue" stackId="1" stroke="#FE4A4A" fill="#FE7C7C" />
        <Area type="monotone" name="Not Flagged" dataKey="flaggedFalse" stackId="1" stroke="#3B69FF" fill="#6F90FF" />
        <Bar type="monotone" name="Total" dataKey="total" barSize={20} fill="#00000088" />
      </ComposedChart>
    </ResponsiveContainer>
  );
}