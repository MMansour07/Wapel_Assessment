using System.Collections.Generic;

namespace EMS.Core.Model
{
    public class TaskCriteria : BaseEntity
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public virtual ICollection<Task> Tasks { get; set; }
    }
}
