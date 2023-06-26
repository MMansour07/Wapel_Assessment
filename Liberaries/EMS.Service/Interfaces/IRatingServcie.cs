using EMS.Core.Dtos.General;
using EMS.Core.Dtos.Rating;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace EMS.Service.Interfaces
{
    public interface IRatingServcie
    {
        Task<ResponseModel<NewRatingDto>> CreateRatingAsync(NewRatingDto obj);
        Task<ResponseModel<List<RatingDto>>> GetRatings(string UserId);

        Task<ResponseModel<NewRatingDto>> GetRatingInfoAsync(int id);
    }
}
