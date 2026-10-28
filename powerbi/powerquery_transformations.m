let
    // Power Query M Script for SharePoint FinanceRequests List Ingestion
    // Author: Ahmad Fathin Naufal (UGM) - System Developer
    Source = Csv.Document(File.Contents("data/processed/finance_requests_300.csv"),[Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"RequestID", type text},
        {"Title", type text},
        {"DocumentType", type text},
        {"RequesterID", type text},
        {"RequesterName", type text},
        {"Department", type text},
        {"CostCenterCode", type text},
        {"AmountIDR", type number},
        {"ApprovalTier", type text},
        {"Status", type text},
        {"SubmissionDate", type datetime},
        {"DueDate", type datetime},
        {"CompletionDate", type datetime},
        {"IsOverdue", type logical},
        {"IsIncomplete", type logical},
        {"SystemPhase", type text},
        {"TurnaroundHours", type number}
    }),
    #"Added SLA Target Hours" = Table.AddColumn(#"Changed Type", "SLATargetHours", each 
        if [ApprovalTier] = "Tier 1 (<= 5M)" then 24
        else if [ApprovalTier] = "Tier 2 (5M - 25M)" then 48
        else 72, Int64.Type
    ),
    #"Added Efficiency Index" = Table.AddColumn(#"Added SLA Target Hours", "TurnaroundRatio", each 
        [TurnaroundHours] / [SLATargetHours], type number
    )
in
    #"Added Efficiency Index"
