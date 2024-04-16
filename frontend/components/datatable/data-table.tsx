"use client";

import * as React from "react";
import {
  ColumnDef,
  ColumnFiltersState,
  Row,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import TData from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { DataTablePagination } from "./data-table-pagination";
import { DataTableToolbar } from "./data-table-toolbar";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "../ui/collapsible";
import { ChevronDown } from "lucide-react";
import { Gauge } from "../ui/guage";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export function DataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const [rowSelection, setRowSelection] = React.useState({});
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({});
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );
  const [sorting, setSorting] = React.useState<SortingState>([]);

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnVisibility,
      rowSelection,
      columnFilters,
    },
    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  });

  return (
    <div className="space-y-4">
      <DataTableToolbar table={table} />
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id} colSpan={header.colSpan}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row: any) => (
                <Collapsible key={row.id} asChild>
                  <>
                    <TableRow
                      key={row.id}
                      data-state={row.getIsSelected() && "selected"}
                    >
                      {row.getVisibleCells().map((cell: any) => (
                        <TableCell key={cell.id}>
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </TableCell>
                      ))}

                      <CollapsibleTrigger asChild>
                        <TableCell className="flex justify-center items-center">
                          <ChevronDown className="cursor-pointer" />
                        </TableCell>
                      </CollapsibleTrigger>
                    </TableRow>
                    <CollapsibleContent asChild>
                      <>
                        <TableRow>
                          <TableCell>Model&nbsp;1&nbsp;Score:</TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center w-[15rem]">
                              <Gauge value={Math.ceil(row.original.model_scores.model_1*100)} size="small" showValue={true} />
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <span className="text-nowrap">{`v${row.original.model_versions.model_1}`}</span>
                            </div>
                          </TableCell>
                        </TableRow>
                        <TableRow>

                        <TableCell>Model&nbsp;2&nbsp;Score:</TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                            <Gauge value={Math.ceil(row.original.model_scores.model_2*100)} size="small" showValue={true} />
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <span className="text-nowrap">{`v${row.original.model_versions.model_2}`}</span>
                            </div>
                          </TableCell>
                        </TableRow>
                        <TableRow>

                        <TableCell>Model&nbsp;3&nbsp;Score:</TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <Gauge value={Math.ceil(row.original.model_scores.model_3*100)} size="small" showValue={true} />
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <span className="text-nowrap">{`v${row.original.model_versions.model_3}`}</span>
                            </div>
                          </TableCell>
                        </TableRow>
                        <TableRow>

                        <TableCell>Model&nbsp;4&nbsp;Score:</TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <Gauge value={Math.ceil(row.original.model_scores.model_4*100)} size="small" showValue={true} />
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <span className="text-nowrap">{`v${row.original.model_versions.model_4}`}</span>
                            </div>
                          </TableCell>
                        </TableRow>
                        <TableRow>

                          <TableCell>Model&nbsp;5&nbsp;Score:</TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <Gauge value={Math.ceil(row.original.model_scores.model_5*100)} size="small" showValue={true} />
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <span className="text-nowrap">{`v${row.original.model_versions.model_5}`}</span>
                            </div>
                          </TableCell>
                        </TableRow>
                        <TableRow>

                        <TableCell>Model&nbsp;6&nbsp;Score:</TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <Gauge value={Math.ceil(row.original.model_scores.model_6*100)} size="small" showValue={true} />
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <span className="text-nowrap">{`v${row.original.model_versions.model_6}`}</span>
                            </div>
                          </TableCell>
                        </TableRow>
                        <TableRow>

                          <TableCell>Utilities</TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <span className="text-nowrap">{`Scraper: v${row.original.scraper_version}`}</span>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-col items-center justify-center">
                              <span className="text-nowrap">{`Cleaner: v${row.original.cleaner_version}`}</span>
                            </div>
                          </TableCell>
                        </TableRow>
                      </>
                    </CollapsibleContent>
                  </>
                </Collapsible>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <DataTablePagination table={table} />
    </div>
  );
}
