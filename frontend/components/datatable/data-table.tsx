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
} from "@/components/ui/collapsible";
import { Gauge } from "@/components/ui/guage";
import { cn } from "@/lib/utils";
import { MagnifyingGlassIcon } from "@radix-ui/react-icons";

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
  const [globalFilter, setGlobalFilter] = React.useState<string>("");

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnVisibility,
      rowSelection,
      columnFilters,
      globalFilter,
    },
    onGlobalFilterChange: setGlobalFilter,
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
    <div className="space-y-4 overflow-x-scroll w-screen md:w-full">
      <DataTableToolbar<TData>
        table={table}
        globalFilter={globalFilter}
        setGlobalFilter={setGlobalFilter}
      />
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
                        <TableCell key={cell.id} className={cn(cell.column.id==="riskscore" ? "flex flex-row" : "")}>
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                          {cell.column.id === "riskscore" && (
                            <CollapsibleTrigger asChild>
                              <TableCell className="flex justify-center items-center h-[3.45rem] px-0">
                                <MagnifyingGlassIcon className="cursor-pointer h-5 w-5 -translate-x-2" />
                              </TableCell>
                            </CollapsibleTrigger>
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                    <CollapsibleContent asChild>
                      <>
                        <TableRow className="border-none">
                          <TableCell></TableCell>
                          <TableCell>
                            <div className="flex flex-row items-center justify-start gap-4 w-[5rem]">
                              {row.original.model_scores.model_1 === -1 ? (
                                <span>
                                  Model&nbsp;1&nbsp;not&nbsp;evaluated
                                </span>
                              ) : (
                                <>
                                  <span>Model&nbsp;1:</span>
                                  <span className="flex flex-row items-center justify-center gap-2">
                                    <Gauge
                                      value={Math.ceil(
                                        row.original.model_scores.model_1 * 100
                                      )}
                                      size="small"
                                      showValue={true}
                                    />
                                    <span className="text-nowrap">{`(v${row.original.model_versions.model_1})`}</span>
                                  </span>
                                </>
                              )}
                            </div>
                          </TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                        </TableRow>
                        <TableRow className="border-none">
                          <TableCell></TableCell>
                          <TableCell>
                            <div className="flex flex-row items-center justify-start gap-4 w-[5rem]">
                              {row.original.model_scores.model_2 === -1 ? (
                                <span>
                                  Model&nbsp;2&nbsp;not&nbsp;evaluated
                                </span>
                              ) : (
                                <>
                                  <span>Model&nbsp;2:</span>
                                  <span className="flex flex-row items-center justify-center gap-2">
                                    <Gauge
                                      value={Math.ceil(
                                        row.original.model_scores.model_2 * 100
                                      )}
                                      size="small"
                                      showValue={true}
                                    />
                                    <span className="text-nowrap">{`(v${row.original.model_versions.model_2})`}</span>
                                  </span>
                                </>
                              )}
                            </div>
                          </TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                        </TableRow>
                        <TableRow className="border-none">
                          <TableCell></TableCell>
                          <TableCell>
                            <div className="flex flex-row items-center justify-start gap-4 w-[5rem]">
                              {row.original.model_scores.model_3 === -1 ? (
                                <span>
                                  Model&nbsp;3&nbsp;not&nbsp;evaluated
                                </span>
                              ) : (
                                <>
                                  <span>Model&nbsp;3:</span>
                                  <span className="flex flex-row items-center justify-center gap-2">
                                    <Gauge
                                      value={Math.ceil(
                                        row.original.model_scores.model_3 * 100
                                      )}
                                      size="small"
                                      showValue={true}
                                    />
                                    <span className="text-nowrap">{`(v${row.original.model_versions.model_3})`}</span>
                                  </span>
                                </>
                              )}
                            </div>
                          </TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                        </TableRow>
                        <TableRow className="border-none">
                          <TableCell></TableCell>
                          <TableCell>
                            <div className="flex flex-row items-center justify-start gap-4 w-[5rem]">
                              {row.original.model_scores.model_4 === -1 ? (
                                <span>
                                  Model&nbsp;4&nbsp;not&nbsp;evaluated
                                </span>
                              ) : (
                                <>
                                  <span>Model&nbsp;4:</span>
                                  <span className="flex flex-row items-center justify-center gap-2">
                                    <Gauge
                                      value={Math.ceil(
                                        row.original.model_scores.model_4 * 100
                                      )}
                                      size="small"
                                      showValue={true}
                                    />
                                    <span className="text-nowrap">{`(v${row.original.model_versions.model_4})`}</span>
                                  </span>
                                </>
                              )}
                            </div>
                          </TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                        </TableRow>
                        <TableRow className="border-none">
                          <TableCell></TableCell>
                          <TableCell>
                            <div className="flex flex-row items-center justify-start gap-4 w-[5rem]">
                              {row.original.model_scores.model_5 === -1 ? (
                                <span>
                                  Model&nbsp;5&nbsp;not&nbsp;evaluated
                                </span>
                              ) : (
                                <>
                                  <span>Model&nbsp;5:</span>
                                  <span className="flex flex-row items-center justify-center gap-2">
                                    <Gauge
                                      value={Math.ceil(
                                        row.original.model_scores.model_5 * 100
                                      )}
                                      size="small"
                                      showValue={true}
                                    />
                                    <span className="text-nowrap">{`(v${row.original.model_versions.model_5})`}</span>
                                  </span>
                                </>
                              )}
                            </div>
                          </TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                        </TableRow>
                        <TableRow className="border-b border-dashed border-opacity-5">
                          <TableCell></TableCell>
                          <TableCell>
                            <div className="flex flex-row items-center justify-start gap-4 w-[5rem]">
                              {row.original.model_scores.model_6 === -1 ? (
                                <span>
                                  Model&nbsp;6&nbsp;not&nbsp;evaluated
                                </span>
                              ) : (
                                <>
                                  <span>Model&nbsp;6:</span>
                                  <span className="flex flex-row items-center justify-center gap-2">
                                    <Gauge
                                      value={Math.ceil(
                                        row.original.model_scores.model_6 * 100
                                      )}
                                      size="small"
                                      showValue={true}
                                    />
                                    <span className="text-nowrap">{`(v${row.original.model_versions.model_6})`}</span>
                                  </span>
                                </>
                              )}
                            </div>
                          </TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                        </TableRow>

                        <TableRow>
                          <TableCell></TableCell>
                          <TableCell>
                            <div className="flex flex-col items-start justify-center">
                              <span className="text-nowrap">{`Scraper: v${row.original.scraper_version}`}</span>
                              <span className="text-nowrap">{`Cleaner: v${row.original.cleaner_version}`}</span>
                            </div>
                          </TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
                          <TableCell></TableCell>
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
