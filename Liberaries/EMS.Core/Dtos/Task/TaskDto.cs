using EMS.Core.Dtos.User;

namespace EMS.Core.Dtos.Task
{
    public class TaskDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public int TaskCriteriaId { get; set; }
        public string UserId { get; set; }
    }
}