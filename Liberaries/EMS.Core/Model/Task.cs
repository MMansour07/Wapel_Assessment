namespace EMS.Core.Model
{
    public class Task : BaseEntity
    {
        public string Name { get; set; }
        public string Details { get; set; }
        public string SuccessIndicator { get; set; }
        public string ActualAccomplishment { get; set; }
        public int TaskCriteriaId { get; set; }
        public virtual TaskCriteria TaskCriteria { get; set; }
        public string UserId { get; set; }
        public virtual User User { get; set; }
    }
}
