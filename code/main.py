import pandas as pd
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from classifier import classify_ticket
from retriever import Retriever

console = Console()


def filter_docs_by_domain(all_docs, company):
    if company == "Visa":
        return [d for d in all_docs if "visa" in d.lower()]
    elif company == "Claude":
        return [d for d in all_docs if "claude" in d.lower()]
    elif company == "HackerRank":
        return [d for d in all_docs if "hackerrank" in d.lower()]
    return all_docs


def generate_response(classification, issue, subject, retriever, docs):
    query = (str(issue) + " " + str(subject or "")).strip()

    # Domain filtering
    filtered_docs = filter_docs_by_domain(docs, classification.company)
    if not filtered_docs:
        filtered_docs = docs

    temp_retriever = Retriever(filtered_docs)
    retrieved_docs = temp_retriever.retrieve(query, k=2)

    # 🔴 Escalation (SAFE)
    if classification.status == "Escalated":
        return (
            "This issue involves sensitive or high-risk information. "
            "It has been escalated to our support team for further review.",
            "Escalated"
        )

    # 🟢 Normal response
    if retrieved_docs:
        doc = retrieved_docs[0].strip()

        # ✅ FIX: Clean prefix handling
        if classification.company and classification.company != "None":
            prefix = f"According to official {classification.company} support documentation:"
        else:
            prefix = "According to official support documentation:"

        return (
            f"{prefix}\n{doc}",
            doc
        )

    # ⚠️ fallback
    return (
        "No relevant information found in support documentation. Please contact support.",
        "N/A"
    )


def main():
    console.print(Panel.fit(
        "[bold green]TRIAGE AGENT (FINAL VERSION)[/bold green]\nClean, Safe, RAG-based",
        title="Status"
    ))

    # Load input
    input_path = "../support_tickets/support_tickets.csv"
    df = pd.read_csv(input_path)
    console.print(f"✅ Loaded {len(df)} tickets")

    # Load corpus
    corpus_path = "../support_tickets/corpus.txt"
    with open(corpus_path, "r", encoding="utf-8") as f:
        docs = [line.strip() for line in f if line.strip()]

    retriever = Retriever(docs)

    results = []

    with Progress(SpinnerColumn(), TextColumn("{task.description}")) as progress:
        task = progress.add_task("Processing tickets...", total=len(df))

        for idx, row in df.iterrows():
            issue = str(row.get('Issue', ''))
            subject = str(row.get('Subject', ''))

            cls = classify_ticket(issue, subject)

            response, source = generate_response(cls, issue, subject, retriever, docs)

            decision = "escalate" if cls.status == "Escalated" else "answer"

            results.append({
                "ticket_id": int(idx),
                "request_type": cls.request_type,
                "product_area": cls.product_area,
                "decision": decision,
                "response": response.strip(),
                "source": source.strip() if isinstance(source, str) else "N/A"
            })

            progress.update(task, advance=1)

    # Save output
    output_path = "../support_tickets/output.csv"
    pd.DataFrame(results).to_csv(output_path, index=False)

    # Save log
    log_path = "../support_tickets/log.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Run completed at {datetime.now()}\n\n")
        for r in results:
            f.write(str(r) + "\n\n")

    console.print("[bold green]✅ Completed! Ready for submission[/bold green]")


if __name__ == "__main__":
    main()