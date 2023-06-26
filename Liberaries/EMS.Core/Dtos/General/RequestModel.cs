using EMS.Core.Interfaces;


namespace EMS.Core.Dtos.General
{
    public class RequestModel<T> : IRequestModel
    {
        public T Data { get; set; }
        public Pagination pagination { get; set; }
        public Sort sort { get; set; }
        public Query query { get; set; }
    }


}
