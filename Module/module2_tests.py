import unittest
import pandas
import module2_utils as tides


class TestDataPlotting(unittest.TestCase):

    #def testGoogleMapworks(self):
    #    import gmaps
    # Check that I can load the google map of the stations
    #    stamap = tides.add_station_maps()
    #    self.assertIs(type(stamap), gmaps.maps.Map)
    #def testGoogleMapsfails(self):
    #   stamap = tides.add_station_maps(API="Stuff")
    #  self.assertTrue(stamap == None)

    def testCreateTideDataset(self):
        import xarray
        # Generate the tidal dataset
        NB = tides.load_Neah_Bay('../Data/')
        PA = tides.load_Port_Angeles('../Data/')
        PT = tides.load_Port_Townsend('../Data/')
        # Create the XArray dataset
        Tides = tides.create_tide_dataset(NB, PA, PT)
        # Check that it is an xarray DataSet
        self.assertIs(type(Tides), xarray.core.dataset.Dataset)

    def testTideDatasetfails(self):
        # Generate the tidal dataset
        NB = tides.load_Neah_Bay('../Data/')
        PA = tides.load_Port_Angeles('../Data/')
        PT = None
        # Don't load all of the Data Arrays
        Tides = tides.create_tide_dataset(NB, PA, None)
        self.assertTrue(Tides == None)

    def testPlotTideDataIndexFails(self):
        NB = tides.load_Neah_Bay('../Data/')
        PA = tides.load_Port_Angeles('../Data/')
        PT = tides.load_Port_Townsend('../Data/')
        # Create the XArray dataset
        Tides = tides.create_tide_dataset(NB, PA, PT)
        # Test that time selection is below available times
        self.assertRaises(IndexError, tides.plot_tide_data, Tides,
                             '2012','2013')
        # Test when time selection is above time range
        self.assertRaises(IndexError, tides.plot_tide_data, Tides,
                             '2017','2018')
        # Test when the times are switched
        self.assertRaises(IndexError, tides.plot_tide_data, Tides,
                             '2016','2015')


    def testPlotTidalElevation(self):
    	NB = tides.load_Neah_Bay('../Data/')
        PA = tides.load_Port_Angeles('../Data/')
        PT = tides.load_Port_Townsend('../Data/')
        # Create the XArray dataset
        Tides = tides.create_tide_dataset(NB, PA, PT)
        # Generate DataArrays with time selection
        NB = Tides.NeahBay.sel(datetime=slice('2015', '2016'))
        PA = Tides.PortAngeles.sel(datetime=slice('2015', '2016'))
        PT = Tides.PortTownsend.sel(datetime=slice('2015', '2016'))


if __name__ == '__main__':
    unittest.main()
