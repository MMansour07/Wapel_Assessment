namespace EMS.Core.Interfaces
{
    public interface IRequestModel
    {
        Pagination pagination { get; set; }
        Sort sort { get; set; }
        Query query { get; set; }
    }
    public class Pagination
    {
        public int page { get; set; }
        public int perpage { get; set; }
    }
    public class Sort
    {
        public string sort { get; set; }
        public string field { get; set; }
    }
    public class Query
    {
        public string generalSearch { get; set; }
    }
}
