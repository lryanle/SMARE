"use client"

import { ColumnDef } from "@tanstack/react-table"

// import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"

import { marketplaces, makes, models, years } from "@/components/datatable/data"
import { Listing } from "@/components/datatable/schema"
import { DataTableColumnHeader } from "./data-table-column-header"
import { DataTableRowActions } from "./data-table-row-actions"
import Link from "next/link";
import { Gauge } from "@/components/ui/guage";

export const columns: ColumnDef<Listing>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
        className="translate-y-[2px]"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
        className="translate-y-[2px] space-x-4"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "id",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="ID" />
    ),
    cell: ({ row }) => <div className="w-[150px]">{row.getValue("id")}</div>,
    enableSorting: false,
    enableHiding: false,
  },
  // {
  //   accessorKey: "title",
  //   header: ({ column }) => (
  //     <DataTableColumnHeader column={column} title="Title" />
  //   ),
  //   cell: ({ row }) => {
  //     const label = labels.find((label) => label.value === row.original.label)

  //     return (
  //       <div className="flex space-x-2">
  //         {label && <Badge variant="outline">{label.label}</Badge>}
  //         <span className="max-w-[500px] truncate font-medium">
  //           {row.getValue("title")}
  //         </span>
  //       </div>
  //     )
  //   },
  // },
  {
    accessorKey: "make",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Make" />
    ),
    cell: ({ row }) => {
      const make = makes.find(
        (make) => make.value === row.getValue("make")
      )

      if (!make) {
        return null
      }

      return (
        <div className="flex w-[100px] items-center">
          {/* {make.icon && (
            <make.icon className="mr-2 h-4 w-4 text-muted-foreground" />
          )} */}
          <span>{make.label}</span>
        </div>
      )
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },
  {
    accessorKey: "model",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Model" />
    ),
    cell: ({ row }) => {
      const model = models.find(
        (model) => model.value === row.getValue("model")
      )

      if (!model) {
        return null
      }

      return (
        <div className="flex w-[200px] items-center">
          {/* {model.icon && (
            <model.icon className="mr-2 h-4 w-4 text-muted-foreground" />
          )} */}
          <span>{model.label}</span>
        </div>
      )
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },
  {
    accessorKey: "year",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Year" />
    ),
    cell: ({ row }) => {
      const year = years.find(
        (year) => year.value === row.getValue("year")
      )

      if (!year) {
        return null
      }

      return (
        <div className="flex w-[50px] items-center">
          {/* {year.icon && (
            <year.icon className="mr-2 h-4 w-4 text-muted-foreground" />
          )} */}
          <span>{year.label}</span>
        </div>
      )
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },
  {
    accessorKey: "riskscore",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Risk Score" />
    ),
    cell: ({ row }) => {
      const riskscore = parseFloat(row.getValue("riskscore"))

      if (!riskscore) {
        return null
      }

      return (
        <div className="flex w-[50px] items-center">
          {/* {riskscore.icon && (
            <riskscore.icon className="mr-2 h-4 w-4 text-muted-foreground" />
          )}
          <span>{riskscore.label}</span> */}
          <Gauge value={Math.ceil(riskscore)} size="small" showValue={true} />
          {/* <span>{parseFloat(String(riskscore)).toFixed(2)}%</span> */}
        </div>
      )
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },
  {
    accessorKey: "date",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Date" />
    ),
    cell: ({ row }) => {
      console.log(row.getValue("date"))
      const date = new Date(String(row.getValue("date"))).toLocaleString("en-US", {  
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "numeric",
        minute: "numeric",
        timeZoneName: "short"
      });

      if (!date) {
        return null
      }

      return (
        <div className="flex w-[100px] items-center">
          {/* {date.icon && (
            <date.icon className="mr-2 h-4 w-4 text-muted-foreground" />
          )}
          <span>{date.label}</span> */}
          <span>{date}</span>
        </div>
      )
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },
  {
    accessorKey: "marketplace",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Marketplace" />
    ),
    cell: ({ row }) => {
      const marketplace = marketplaces.find(
        (marketplace) => marketplace.value === row.getValue("marketplace")
      )
      const url = String(row.original.url)

      if (!marketplace) {
        return null
      }

      if (!url) {
        return null
      }

      return (
        <div className="flex w-[100px] items-center">
          {marketplace.icon && (
            <marketplace.icon className="mr-2 h-4 w-4 text-muted-foreground" />
          )}
          <Link href={url} target="_blank">{marketplace.label}</Link>
        </div>
      )
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },
  // {
  //   id: "actions",
  //   cell: ({ row }) => <DataTableRowActions row={row} />,
  // },
]
