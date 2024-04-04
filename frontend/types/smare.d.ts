export type scrapeListing = {
  _id: string;
  title: string;
  price: number;
  odometer: number;
  link: string;
  location?: string;
  website?: string;
  post_body: string;
  year: number;
  makemodel?: string;
  latitude?: number;
  longitude?: number;
  attributes?: Object[];
  images: string[];
  source: string;
  scraper_version: number;
  scrape_date: string;
  stage: string;
  cleaner_version: number;
  make: string;
  model: string;
  model_scores: { model_1: number; model_2: number; model_3: number; model_4: number; model_5: number; model_6: number; }
  model_versions: { model_1: number; model_2: number; model_3: number; model_4: number; model_5: number; model_6: number; }
  risk_score: number;
  pending_risk_update: boolean;
  flagged: number;
};

export type displayListing = {
  source: string;
  make: string;
  model: string;
  year: number;
  scrape_date: string;
  risk_score: number;
}

export type dashboardCardTypes = {
  totalListings: number;
  riskScoreOver50: number;
  listingsThisWeek: number;
  percentIncreaseThisMonth: number;
  percentIncreaseRiskScoreThisMonth: number;
  percentIncreaseLastMonth: number;
  listingsToday: number;
  listingsThisMonth: number;
  listingsLastMonth: number;
};
