import { describe, expect, it } from "vitest";
import { canDecide } from "./workflow";

describe("human gate affordances", () => {
  it("shows approvals only in review states", () => {
    expect(canDecide("DATA_REVIEW", "APPROVE")).toBe(true);
    expect(canDecide("ANALYSIS_REVIEW", "APPROVE")).toBe(true);
    expect(canDecide("ANALYZING", "APPROVE")).toBe(false);
  });

  it("does not offer go-back before research starts", () => {
    expect(canDecide("DRAFT", "GO_BACK")).toBe(false);
    expect(canDecide("DATA_REVIEW", "GO_BACK")).toBe(true);
  });
});
