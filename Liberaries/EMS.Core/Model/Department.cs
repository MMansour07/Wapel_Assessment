using System.Collections.Generic;

namespace EMS.Core.Model
{
    public class Department : BaseEntity
    {
        public string Title { get; set; }
        public string Description { get; set; }
        public virtual ICollection<User> Users { get; set; }
    }
}
