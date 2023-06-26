using EMS.Core.Dtos.General;
using System.Threading.Tasks;
using System.Collections.Generic;
using EMS.Core.Dtos.Department;

namespace EMS.Service.Interfaces
{
    public interface IDepartmentService
    {
        Task<ResponseModel<List<DepartmentDto>>> GetDeparments();
    }
}
