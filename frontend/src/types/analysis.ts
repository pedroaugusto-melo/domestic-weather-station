export interface Suggestion {
  title: string;
  description: string;
}

export interface AnalysisResponse {
  suggestions: Suggestion[];
} 