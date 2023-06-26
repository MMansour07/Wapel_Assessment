using AutoMapper;
using EMS.Core.Dtos.General;
using EMS.Core.Dtos.Evaluation;
using EMS.Core.Interfaces;
using EMS.Core.Model;
using EMS.Service.Interfaces;
using System.Linq;
using System.Threading.Tasks;
using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Net;

namespace EMS.Service.Services
{
    public class EvaluationService : IEvaluationService
    {
        private readonly IUnitOfWork _unitOfWork;
        private IMapper _autoMapper;
        public EvaluationService(IMapper autoMapper, IUnitOfWork unitOfWork)
        {
            _autoMapper = autoMapper;
            _unitOfWork = unitOfWork;
        }

        public Task<ResponseModel<NewEvaluationDto>> CreateEvaluationAsync(NewEvaluationDto obj)
        {
            throw new NotImplementedException();
        }

        public Task<ResponseModel<int>> DeleteAllEvaluations(string userId)
        {
            throw new NotImplementedException();
        }

        public Task<ResponseModel<int>> DeleteEvaluation(int id)
        {
            throw new NotImplementedException();
        }

        public Task<ResponseModel<EditEvaluationPostDto>> EditEvaluationAsync(EditEvaluationPostDto obj)
        {
            throw new NotImplementedException();
        }

        public Task<ResponseModel<EditEvaluationDto>> FindEvaluationAsync(int Id)
        {
            throw new NotImplementedException();
        }

        public Task<ResponseModel<TableModel<EvaluationDto>>> GetEvaluationsByUserIdAsync(RequestModel<string> obj)
        {
            throw new NotImplementedException();
        }
        //public async Task<ResponseModel<TableModel<EvaluationDto>>> GetEvaluationsByUserIdAsync(RequestModel<string> obj)
        //{
        //    try
        //    {
        //        var Evaluations = _unitOfWork.evaluationRepository.Filter(i => i.UserId == obj.Data, obj.sort, obj.query, i => i.Title.ToLower().Contains(obj.query.generalSearch));
        //        return new ResponseModel<TableModel<EvaluationDto>>()
        //        {
        //            Success = true,
        //            Data = _autoMapper.Map<PagedList<Evaluation>, TableModel<EvaluationDto>>(await PagedList<Evaluation>.Create(Evaluations, obj.pagination.page, obj.pagination.perpage, Evaluations.Count()))
        //        };
        //    }
        //    catch (Exception ex)
        //    {
        //        //logs + roll back
        //        return new ResponseModel<TableModel<EvaluationDto>>() { Ex = ex, Message = ex.Message, Success = false };
        //    }
        //}

        //public async Task<ResponseModel<NewEvaluationDto>> CreateEvaluationAsync(NewEvaluationDto obj)
        //{
        //    try
        //    {
        //        Cloudinary _cloudinary = new Cloudinary(new Account()
        //        {
        //            Cloud = ConfigurationManager.AppSettings["CloudName"],
        //            ApiKey = ConfigurationManager.AppSettings["ApiKey"],
        //            ApiSecret = ConfigurationManager.AppSettings["ApiSecret"],
        //        });

        //        IList<VideoUploadResult> videoUploadResult = new List<VideoUploadResult>();

        //        if (obj.Files?.Count > 0)
        //        {
        //            for (int i = 0; i < obj.Files.Count; i++)
        //            {
        //                using (var stream = obj.Files[i].InputStream)
        //                {
        //                    var response = await _cloudinary.UploadAsync(new VideoUploadParams() { File = new FileDescription(obj.Files[i].FileName, stream) });
        //                    if (response.StatusCode == HttpStatusCode.OK)
        //                        videoUploadResult.Add(response);
        //                    else
        //                        break;
        //                        // roll back to achieve unit of work
        //                }
        //            }
        //        }

        //        var result =  _unitOfWork.EvaluationRepository.Add(obj.ToEvaluation(obj, _autoMapper.Map<NewEvaluationDto, Evaluation>(obj), _autoMapper.Map<IList<VideoUploadResult>, IList<Media>>(videoUploadResult)));

        //        await _unitOfWork.SaveChanges();

        //        return new ResponseModel<NewEvaluationDto>() { Data = _autoMapper.Map<Evaluation, NewEvaluationDto>(result), Success = true};
        //    }
        //    catch (Exception ex)
        //    {
        //        //logs + roll back
        //        return new ResponseModel<NewEvaluationDto>() {Ex = ex, Message = ex.Message, Success = false };
        //    }
        //}

        //public async Task<ResponseModel<EditEvaluationDto>> FindEvaluationAsync(int Id)
        //{
        //    try
        //    {
        //        return new ResponseModel<EditEvaluationDto>() {Data = _autoMapper.Map<Evaluation, EditEvaluationDto>(await _unitOfWork.EvaluationRepository.FindBy(i => i.Id == Id).FirstOrDefaultAsync()), Success = true };
        //    }
        //    catch (Exception ex)
        //    {
        //        //logs
        //        return new ResponseModel<EditEvaluationDto>() { Ex = ex, Message = ex.Message, Success = false };
        //    }
        //}

        //public async Task<ResponseModel<EditEvaluationPostDto>> EditEvaluationAsync(EditEvaluationPostDto obj)
        //{
        //    try
        //    {
        //        Cloudinary _cloudinary = new Cloudinary(new Account()
        //        {
        //            Cloud = ConfigurationManager.AppSettings["CloudName"],
        //            ApiKey = ConfigurationManager.AppSettings["ApiKey"],
        //            ApiSecret = ConfigurationManager.AppSettings["ApiSecret"],
        //        });

        //        List<VideoUploadResult> videoUploadResult = new List<VideoUploadResult>();
        //        DelResResult delresponse = new DelResResult();

        //        if(obj.PublicIds != null)
        //        {
        //             delresponse = await _cloudinary.DeleteResourcesAsync(ResourceType.Video, obj.PublicIds.ToArray());
        //        }

        //        if (delresponse.StatusCode == HttpStatusCode.OK || obj.PublicIds == null)
        //        {

        //            if (obj.NewFiles != null)
        //            {
        //                for (int i = 0; i < obj.NewFiles.Count; i++)
        //                {
        //                    using (var stream = obj.NewFiles[i].InputStream)
        //                    {
        //                        var response = await _cloudinary.UploadAsync(new VideoUploadParams() { File = new FileDescription(obj.NewFiles[i].FileName, stream) });
        //                        if (response.StatusCode == HttpStatusCode.OK)
        //                            videoUploadResult.Add(response);
        //                        else
        //                            break;
        //                        // roll back to achieve unit of work
        //                    }
        //                }
        //            }
        //            // Yhere is no one update statement for the entity (Evaluation) and its children in Enitiy framowrk / and that is one of the powerful features of entity framework core
        //            if (obj.EliminatedIds != null)
        //            await _unitOfWork.mediaRepository.Delete(i => obj.EliminatedIds.Contains(i.Id));

        //            if (videoUploadResult.Count > 0)
        //                _unitOfWork.mediaRepository.AddRange(obj.ToMedialst(obj, _autoMapper.Map<List<VideoUploadResult>, List<Media>>(videoUploadResult)));

        //            _unitOfWork.mediaRepository.UpdateMedia(obj.Id, obj.Titles, obj.PublicIds);

        //            _unitOfWork.EvaluationRepository.UpdateAsync(_autoMapper.Map<EditEvaluationPostDto, Evaluation>(obj));

        //            await _unitOfWork.SaveChanges();
        //        }
        //        return new ResponseModel<EditEvaluationPostDto>() { Data = obj, Success = true };
        //    }
        //    catch (Exception ex)
        //    {
        //        //logs + roll back
        //        return new ResponseModel<EditEvaluationPostDto>() { Ex = ex, Message = ex.Message, Success = false };
        //    }
        //}


        //public async Task<ResponseModel<int>> DeleteAllEvaluations(string userId)
        //{
        //    try
        //    {
        //        // ask if we should delete video from the cloud or not
        //        // keep tracking uploaded videos before
        //        await _unitOfWork.EvaluationRepository.Delete(i => i.UserId == userId);

        //        return new ResponseModel<int>() { Data = await _unitOfWork.SaveChanges(), Success = true };
        //    }
        //    catch (Exception ex)
        //    {
        //        //logs
        //        return new ResponseModel<int>() { Ex = ex, Message = ex.Message, Success = false };
        //    }
        //}

        //public async Task<ResponseModel<int>> DeleteEvaluation(int id)
        //{
        //    try
        //    {
        //        // ask if we should delete video from the cloud or not
        //        // keep tracking uploaded videos before

        //        await _unitOfWork.EvaluationRepository.Delete(i => i.Id == id);

        //        return new ResponseModel<int>() { Data = await _unitOfWork.SaveChanges(), Success = true };
        //    }
        //    catch (Exception ex)
        //    {
        //        //logs
        //        return new ResponseModel<int>() { Ex = ex, Message = ex.Message, Success = false };
        //    }
        //}

    }
}
