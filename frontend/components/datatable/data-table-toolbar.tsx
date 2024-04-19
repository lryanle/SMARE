"use client";

import { Cross2Icon } from "@radix-ui/react-icons";
import { Table } from "@tanstack/react-table";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTableViewOptions } from "@/components/datatable/data-table-view-options";

import {
  marketplaces,
  makes,
  models,
  years,
} from "@/components/datatable/data";
import { DataTableFacetedFilter } from "@/components/datatable/data-table-faceted-filter";

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
  globalFilter: string;
  setGlobalFilter: (value: string) => void;
}

export function DataTableToolbar<TData>({
  table,
  globalFilter,
  setGlobalFilter,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;

  return (
    <div className="flex items-center justify-between overflow-x-scroll py-2 md:py-0 md:overflow-auto">
      <div className="flex flex-1 items-center space-x-2">
        <Input
          placeholder="Filter listings..."
          value={globalFilter}
          onChange={(event) => {
            setGlobalFilter(event.target.value);
          }}
          className="h-8 w-[150px] lg:w-[250px]"
        />
        {table.getColumn("marketplace") && (
          <DataTableFacetedFilter
            column={table.getColumn("marketplace")}
            title="marketplace"
            options={marketplaces}
          />
        )}
        {table.getColumn("make") && (
          <DataTableFacetedFilter
            column={table.getColumn("make")}
            title="make"
            options={makes}
          />
        )}
        {table.getColumn("model") && (
          <DataTableFacetedFilter
            column={table.getColumn("model")}
            title="model"
            options={models}
          />
        )}
        {table.getColumn("year") && (
          <DataTableFacetedFilter
            column={table.getColumn("year")}
            title="year"
            options={years.map((year) => ({
              label: year.label,
              value: year.value.toString(),
            }))}
          />
        )}
        {/* TODO: Datetime selector here */}
        {/* TODO: Risk score slider selector here */}
        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => table.resetColumnFilters()}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <Cross2Icon className="ml-2 h-4 w-4" />
          </Button>
        )}
      </div>
      <DataTableViewOptions table={table} />
    </div>
  );
}
