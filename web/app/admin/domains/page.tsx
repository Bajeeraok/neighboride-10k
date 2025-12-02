// Simple admin page to add domains
export default function Domains() {
  return (
    <div className="p-8">
      <h1 className="text-3xl mb-6">Manage Company Domains</h1>
      <form className="bg-white p-6 rounded shadow">
        <input placeholder="company.com" className="border p-3 w-64" />
        <input placeholder="Company Name" className="border p-3 w-64 ml-4" />
        <button className="bg-green-600 text-white px-6 py-3 ml-4 rounded">Add Domain</button>
      </form>
      <table className="mt-8 w-full">
        <thead><tr><th>Domain</th><th>Company</th><th>Actions</th></tr></thead>
        <tbody>
          <tr><td>@wellsfargo.com</td><td>Wells Fargo</td><td><button>Remove</button></td></tr>
          <tr><td>@charlotte.edu</td><td>UNC Charlotte</td><td><button>Remove</button></td></tr>
        </tbody>
      </table>
    </div>
  );
}