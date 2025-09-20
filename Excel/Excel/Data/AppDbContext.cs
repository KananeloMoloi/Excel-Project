using Excel.Models;
using Microsoft.EntityFrameworkCore;

namespace Excel.Data
{
	public class AppDbContext : DbContext
	{
		public AppDbContext(DbContextOptions options) : base(options)
		{
		}

		public DbSet<Users> Users { get; set; }
		public DbSet<Records> Records { get; set; }
	}
}
