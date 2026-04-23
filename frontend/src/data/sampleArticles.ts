export type SampleArticle = {
  slug: string;
  label: string;
  title: string;
  body: string;
};

export const sampleArticles: SampleArticle[] = [
  {
    slug: "city-budget",
    label: "Local Accountability",
    title: "City council releases line-item budget after public pressure",
    body:
      "The city council published a full draft budget Tuesday night, including departmental spending, planned hiring, and capital projects. Reporters verified the figures against meeting packets and interviewed both council members and neighborhood advocates about the tradeoffs in the plan."
  },
  {
    slug: "celebrity-rumor",
    label: "High-Risk Framing",
    title: "SHOCKING EXCLUSIVE: celebrity secretly funds miracle cure after media blackout!!!",
    body:
      "A viral post claims unnamed insiders exposed a hidden medical breakthrough being buried by major news outlets. The article cites no documents, no named experts, and relies heavily on dramatic language instead of verifiable sourcing."
  },
  {
    slug: "election-brief",
    label: "Ambiguous Signal",
    title: "Election fraud claims spread online before official county audit",
    body:
      "Several social posts alleged widespread irregularities after early returns were delayed. County officials later said the delay came from a damaged ballot scanner and said a full audit log would be released within 48 hours, leaving the situation unresolved at publication time."
  }
];
