using EMS.Core.Dtos.General;
using EMS.Core.Dtos.Evaluation;
using System.Threading.Tasks;

namespace EMS.Service.Interfaces
{
    public interface IEvaluationService
    {
        Task<ResponseModel<TableModel<EvaluationDto>>> GetEvaluationsByUserIdAsync(RequestModel<string> obj);
        Task<ResponseModel<NewEvaluationDto>> CreateEvaluationAsync(NewEvaluationDto obj);
        Task<ResponseModel<EditEvaluationDto>> FindEvaluationAsync(int Id);
        Task<ResponseModel<EditEvaluationPostDto>> EditEvaluationAsync(EditEvaluationPostDto obj);
        Task<ResponseModel<int>> DeleteAllEvaluations(string userId);
        Task<ResponseModel<int>> DeleteEvaluation(int id);
    }
}
