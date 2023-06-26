using EMS.Core.Dtos.General;
using EMS.Core.Dtos.Task;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace EMS.Service.Interfaces
{
    public interface ITaskServcie
    {
        Task<ResponseModel<NewTaskDto>> CreateTaskAsync(NewTaskDto obj);
        Task<ResponseModel<List<TaskDto>>> GetTasksByCriteriaId(int TaskCriteriaId);
    }
}
