export default function HomePage() {
  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand"><span className="brand-mark">TT</span> TRUST TRASH</div>
        <span className="status"><i /> Foundation starter</span>
      </header>
      <section className="hero">
        <p className="eyebrow">UNIFIED DATA INTELLIGENCE PLATFORM</p>
        <h1>One query.<br /><span>Connected data.</span></h1>
        <p className="intro">
          Discover, retrieve and understand information across the sources you connect.
        </p>
        <div className="searchBox">
          <span>⌕</span>
          <input aria-label="Search" placeholder="Search connected sources…" disabled />
          <button disabled>Search</button>
        </div>
        <p className="hint">Search is a placeholder in this foundation build. Connectors and query execution are not implemented yet.</p>
      </section>
      <section className="grid">
        {[
          ["01", "Connections", "Cloud, databases, websites and development tools."],
          ["02", "Discovery", "A unified query layer across connected sources."],
          ["03", "Processing", "ETL, documents, OCR, NLP and computer vision."],
          ["04", "Data platform", "Data Lake, Lakehouse and analytical storage."],
        ].map(([number, title, description]) => (
          <article className="card" key={number}>
            <span>{number}</span><h2>{title}</h2><p>{description}</p>
          </article>
        ))}
      </section>
      <footer>Architecture foundation · v0.1.0 · Not a production release</footer>
    </main>
  );
}
