import { date, z } from "zod"

// We're keeping a simple non-relational schema here.
// IRL, you will have a schema for your data models.
export const listingSchema = z.object({
  id: z.string(),
  make: z.string(),
  model: z.string(),
  year: z.number(),
  riskscore: z.number(),
  // url: z.string(),
  marketplace: z.string(),
  date: z.string(),
})

export const rawListingSchema = z.object({
  _id: z.string(),
  make: z.string(),
  model: z.string(),
  year: z.number(),
  risk_score: z.number(),
  link: z.string(),
  source: z.string(),
  scrape_date: z.string(),
})

export type Listing = z.infer<typeof listingSchema>
