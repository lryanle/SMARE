import * as React from "react";
import { format } from "date-fns";
import { Column } from "@tanstack/react-table";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { CalendarIcon } from "@radix-ui/react-icons";

interface DateTableDateFilterProps<TData, TValue> {
  column?: Column<TData, TValue>
  title?: string
  options: {
    label: string
    value: string
    icon?: React.ComponentType<{ className?: string }>
  }[]
}

export function DateTableDateFilter<TData, TValue>({ column }: DateTableDateFilterProps<TData, TValue>) {
  // Initialize the date from the filter value, ensuring it is treated as Date or undefined.
  const [selectedDate, setSelectedDate] = React.useState<Date | undefined>(
    column?.getFilterValue() as Date | undefined
  );

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" className="justify-start text-left h-8 border-dashed text-xs">
          <CalendarIcon className="mr-2 h-4 w-4" />
          {selectedDate ? format(selectedDate, "PPP") : "Pick a date"}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar
          mode="single"
          selected={selectedDate}
          onSelect={(date: Date | undefined) => {
            if (date) {  // Ensure date is not undefined before using it
              setSelectedDate(date);
              column?.setFilterValue(date);
            }
          }}
          initialFocus
        />
      </PopoverContent>
    </Popover>
  );
}
