using EMS.Core.Dtos.General;
using EMS.Core.Dtos.TaskCriteria;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace EMS.Service.Interfaces
{
    public interface ITaskCriteriaServcie
    {
        Task<ResponseModel<NewCriteriaDto>> CreateCriteriaAsync(NewCriteriaDto obj);
        Task<ResponseModel<List<CriteriaDto>>> GetCriterias();
    }
}
