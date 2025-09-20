using System.ComponentModel.DataAnnotations;
using System.Runtime.InteropServices.Marshalling;

namespace Excel.Models
{
	public class Users
	{
		[Key]
		public int user_id { get; set; }
		[Required]
		public string Name { get; set; }


		public virtual ICollection<Records> Records { get; set; }
	}
}
