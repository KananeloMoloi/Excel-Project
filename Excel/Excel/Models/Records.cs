using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Excel.Models
{
	public class Records
	{
		[Key]
		public int record_id { get; set; }

		[Required]
		[ForeignKey("Users")]
		public int user_id { get; set; }

		[Required]
		public int Year {  get; set; }

		[Required]
		public int Month { get; set; }

		[Required]
		public double Amount { get; set; }

		public virtual Users Users { get; set; }
	}
}
