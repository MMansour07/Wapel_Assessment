using EMS.Core.Interfaces;
using System;

namespace EMS.Core.Dtos.General
{
    public class ResponseModel<T> : IResponseModel
    {
        public T Data { get; set; }
        public Exception Ex { get; set; }
        public string Message { get; set; }
        public bool Success { get; set; }
    }
}
