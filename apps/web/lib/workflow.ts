export type HumanDecision = "APPROVE" | "REJECT" | "RESEARCH_MORE" | "GO_BACK";

export function canDecide(state: string, decision: HumanDecision): boolean {
  const review = state === "DATA_REVIEW" || state === "ANALYSIS_REVIEW";
  if (decision === "APPROVE" || decision === "REJECT" || decision === "RESEARCH_MORE") {
    return review;
  }
  return state !== "DRAFT" && state !== "SCOPED";
}
